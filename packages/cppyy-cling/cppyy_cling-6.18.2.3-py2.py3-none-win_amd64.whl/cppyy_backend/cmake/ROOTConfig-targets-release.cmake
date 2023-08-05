#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ROOT::Cling" for configuration "Release"
set_property(TARGET ROOT::Cling APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::Cling PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libCling.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libCling.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::Cling )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::Cling "${_IMPORT_PREFIX}/lib/libCling.lib" "${_IMPORT_PREFIX}/bin/libCling.dll" )

# Import target "ROOT::Thread" for configuration "Release"
set_property(TARGET ROOT::Thread APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::Thread PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libThread.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libThread.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::Thread )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::Thread "${_IMPORT_PREFIX}/lib/libThread.lib" "${_IMPORT_PREFIX}/bin/libThread.dll" )

# Import target "ROOT::Core" for configuration "Release"
set_property(TARGET ROOT::Core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::Core PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libCore.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libCore.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::Core )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::Core "${_IMPORT_PREFIX}/lib/libCore.lib" "${_IMPORT_PREFIX}/bin/libCore.dll" )

# Import target "ROOT::bindexplib" for configuration "Release"
set_property(TARGET ROOT::bindexplib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::bindexplib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/bindexplib.exe"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::bindexplib )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::bindexplib "${_IMPORT_PREFIX}/bin/bindexplib.exe" )

# Import target "ROOT::rmkdepend" for configuration "Release"
set_property(TARGET ROOT::rmkdepend APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::rmkdepend PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/rmkdepend.exe"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::rmkdepend )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::rmkdepend "${_IMPORT_PREFIX}/bin/rmkdepend.exe" )

# Import target "ROOT::MathCore" for configuration "Release"
set_property(TARGET ROOT::MathCore APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::MathCore PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libMathCore.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libMathCore.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::MathCore )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::MathCore "${_IMPORT_PREFIX}/lib/libMathCore.lib" "${_IMPORT_PREFIX}/bin/libMathCore.dll" )

# Import target "ROOT::RIO" for configuration "Release"
set_property(TARGET ROOT::RIO APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::RIO PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/libRIO.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/libRIO.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::RIO )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::RIO "${_IMPORT_PREFIX}/lib/libRIO.lib" "${_IMPORT_PREFIX}/bin/libRIO.dll" )

# Import target "ROOT::rootcling" for configuration "Release"
set_property(TARGET ROOT::rootcling APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ROOT::rootcling PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/rootcling.exe"
  )

list(APPEND _IMPORT_CHECK_TARGETS ROOT::rootcling )
list(APPEND _IMPORT_CHECK_FILES_FOR_ROOT::rootcling "${_IMPORT_PREFIX}/bin/rootcling.exe" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
