from conans import ConanFile, CMake, tools
import os
import shutil


class CUnitConan(ConanFile):
    name = "cunit"
    version = "2.1-3"
    homepage = "http://cunit.sourceforge.net/"
    url = "https://github.com/atolab/conan-cunit"
    description = "A Unit Testing Framework for C"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "snprintf.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': True, 'fPIC': True}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        source_url = "https://sourceforge.net/projects/cunit"
        tools.get("{0}/files/{1}/{2}/{1}-{2}.tar.bz2".format(source_url, "CUnit", self.version))
        extracted_dir = "CUnit-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        shutil.copy("CMakeLists.txt", self._source_subfolder)
        # Do not define snprintf on Windows if _MSC_VER is greater than or
        # equal to 1900.
        tools.patch(patch_file='snprintf.patch')

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder, keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
