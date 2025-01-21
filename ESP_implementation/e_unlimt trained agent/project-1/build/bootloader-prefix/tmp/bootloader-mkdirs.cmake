# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "C:/Users/gianl/esp/v5.2.2/esp-idf/components/bootloader/subproject"
  "C:/Users/gianl/Desktop/Nuova cartella/mu nodiv/einf/project-1/build/bootloader"
  "C:/Users/gianl/Desktop/Nuova cartella/mu nodiv/einf/project-1/build/bootloader-prefix"
  "C:/Users/gianl/Desktop/Nuova cartella/mu nodiv/einf/project-1/build/bootloader-prefix/tmp"
  "C:/Users/gianl/Desktop/Nuova cartella/mu nodiv/einf/project-1/build/bootloader-prefix/src/bootloader-stamp"
  "C:/Users/gianl/Desktop/Nuova cartella/mu nodiv/einf/project-1/build/bootloader-prefix/src"
  "C:/Users/gianl/Desktop/Nuova cartella/mu nodiv/einf/project-1/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Users/gianl/Desktop/Nuova cartella/mu nodiv/einf/project-1/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/Users/gianl/Desktop/Nuova cartella/mu nodiv/einf/project-1/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
