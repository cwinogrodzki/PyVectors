# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/grodzki/.local/lib/python3.10/site-packages/dace/codegen

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /net/myshella/home/grodzki/PyVectors/.dacecache/stencil_kernel/build

# Utility rule file for stencil_kernel_hw.

# Include any custom commands dependencies for this target.
include CMakeFiles/stencil_kernel_hw.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/stencil_kernel_hw.dir/progress.make

CMakeFiles/stencil_kernel_hw:

stencil_kernel_hw: CMakeFiles/stencil_kernel_hw
stencil_kernel_hw: CMakeFiles/stencil_kernel_hw.dir/build.make
.PHONY : stencil_kernel_hw

# Rule to build all files generated by this target.
CMakeFiles/stencil_kernel_hw.dir/build: stencil_kernel_hw
.PHONY : CMakeFiles/stencil_kernel_hw.dir/build

CMakeFiles/stencil_kernel_hw.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/stencil_kernel_hw.dir/cmake_clean.cmake
.PHONY : CMakeFiles/stencil_kernel_hw.dir/clean

CMakeFiles/stencil_kernel_hw.dir/depend:
	cd /net/myshella/home/grodzki/PyVectors/.dacecache/stencil_kernel/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/grodzki/.local/lib/python3.10/site-packages/dace/codegen /home/grodzki/.local/lib/python3.10/site-packages/dace/codegen /net/myshella/home/grodzki/PyVectors/.dacecache/stencil_kernel/build /net/myshella/home/grodzki/PyVectors/.dacecache/stencil_kernel/build /net/myshella/home/grodzki/PyVectors/.dacecache/stencil_kernel/build/CMakeFiles/stencil_kernel_hw.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/stencil_kernel_hw.dir/depend
