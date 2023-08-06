#!/usr/bin/env python
"""An implementation of linux client builder."""
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import fnmatch
import logging
import os
import shutil
import subprocess
import zipfile

from grr_response_client_builder import build
from grr_response_core import config
from grr_response_core.lib import config_lib
from grr_response_core.lib import package
from grr_response_core.lib import utils


class LinuxClientBuilder(build.ClientBuilder):
  """Builder class for the Linux client."""

  def __init__(self, context=None):
    super(LinuxClientBuilder, self).__init__(context=context)

    self.fleetspeak_enabled = config.CONFIG.Get(
        "Client.fleetspeak_enabled", context=self.context)
    # Directory containing files that will be included in the zip template.
    self.package_dir = config.CONFIG.Get(
        "PyInstaller.dpkg_root", context=self.context)
    self.context.append("Target:Linux")

  def StripLibraries(self, directory):
    # TODO(user): this is essentially "dh_strip --exclude=ffi" for deb
    # packages, if we can figure out the equivalent for redhat we could get rid
    # of this code.
    matches = []
    for root, _, filenames in os.walk(directory):
      for filename in fnmatch.filter(filenames, "*.so*"):
        # strip dies with errors on ffi libs, leave them alone.
        if "ffi" not in filename:
          matches.append(os.path.join(root, filename))
    cmd = ["strip"]
    cmd.extend(matches)
    subprocess.check_call(cmd)

  def BuildWithPyInstaller(self):
    super(LinuxClientBuilder, self).BuildWithPyInstaller()
    self.StripLibraries(self.output_dir)

  def MakeExecutableTemplate(self, output_file=None):
    super(LinuxClientBuilder,
          self).MakeExecutableTemplate(output_file=output_file)
    self.MakeBuildDirectory()
    self.CleanDirectory(self.package_dir)
    self.BuildWithPyInstaller()
    self.CopyMissingModules()
    self.CopyFiles()
    if self.fleetspeak_enabled:
      # Include the Fleetspeak service config in the template.
      fleetspeak_dir = os.path.join(self.package_dir, "fleetspeak")
      utils.EnsureDirExists(fleetspeak_dir)
      shutil.copy(
          config.CONFIG.Get(
              "ClientBuilder.fleetspeak_config_path", context=self.context),
          fleetspeak_dir)
    self.MakeZip(self.package_dir, self.template_file)

  def CopyFiles(self):
    """This sets up the template directory."""
    if self.fleetspeak_enabled:
      # Copy files needed for dpkg-buildpackage.
      shutil.copytree(
          config_lib.Resource().Filter(
              "install_data/debian/dpkg_client/fleetspeak-debian"),
          os.path.join(self.package_dir, "debian/debian.in"))
      return

    # Copy the nanny binary.
    shutil.copy(
        package.ResourcePath("grr-response-core",
                             "install_data/debian/dpkg_client/nanny.sh.in"),
        self.output_dir)

    # Copy files needed for dpkg-buildpackage.
    shutil.copytree(
        config_lib.Resource().Filter("install_data/debian/dpkg_client/debian"),
        os.path.join(self.package_dir, "debian/debian.in"))

    # Copy upstart files
    outdir = os.path.join(self.package_dir, "debian/upstart.in")
    utils.EnsureDirExists(outdir)
    shutil.copy(
        config_lib.Resource().Filter(
            "install_data/debian/dpkg_client/upstart/grr-client.conf"), outdir)

    # Copy init files
    outdir = os.path.join(self.package_dir, "debian/initd.in")
    utils.EnsureDirExists(outdir)
    shutil.copy(
        config_lib.Resource().Filter(
            "install_data/debian/dpkg_client/initd/grr-client"), outdir)

    # Copy systemd unit file
    outdir = os.path.join(self.package_dir, "debian/systemd.in")
    utils.EnsureDirExists(outdir)
    shutil.copy(
        config_lib.Resource().Filter(
            "install_data/systemd/client/grr-client.service"), outdir)

  def MakeZip(self, input_dir, output_file):
    """Creates a ZIP archive of the files in the input directory.

    Args:
      input_dir: the name of the input directory.
      output_file: the name of the output ZIP archive without extension.
    """

    logging.info("Generating zip template file at %s", output_file)
    zf = zipfile.ZipFile(output_file, "w")
    oldwd = os.getcwd()
    os.chdir(input_dir)
    for path in ["debian", "rpmbuild", "fleetspeak"]:
      for root, _, files in os.walk(path):
        for f in files:
          zf.write(os.path.join(root, f))
    zf.close()
    os.chdir(oldwd)


class CentosClientBuilder(LinuxClientBuilder):
  """A builder class that produces a client for RPM based distros."""

  def CopyFiles(self):
    """This sets up the template directory."""

    shutil.move(
        os.path.join(self.package_dir, "debian"),
        os.path.join(self.package_dir, "rpmbuild"))
    if self.fleetspeak_enabled:
      rpm_spec_filename = "fleetspeak.grr.spec.in"
    else:
      rpm_spec_filename = "grr.spec.in"
      shutil.copy(
          config_lib.Resource().Filter(
              "install_data/centos/grr-client.initd.in"),
          os.path.join(self.package_dir, "rpmbuild/grr-client.initd.in"))
      shutil.copy(
          config_lib.Resource().Filter(
              "install_data/systemd/client/grr-client.service"),
          os.path.join(self.package_dir, "rpmbuild/grr-client.service.in"))

    shutil.copy(
        config_lib.Resource().Filter("install_data/centos/" +
                                     rpm_spec_filename),
        os.path.join(self.package_dir, "rpmbuild/grr.spec.in"))

    # Copy prelink blacklist file. Without this file, prelink will mangle
    # the GRR binary.
    shutil.copy(
        config_lib.Resource().Filter(
            "install_data/centos/prelink_blacklist.conf.in"),
        os.path.join(self.package_dir, "rpmbuild/prelink_blacklist.conf.in"))
