cmake_minimum_required( VERSION 2.8 )
project( versioning )
enable_testing()

file(GLOB Files 
    ${CMAKE_CURRENT_SOURCE_DIR}/metadata.txt
    ${CMAKE_CURRENT_SOURCE_DIR}/*.py 
    ${CMAKE_CURRENT_SOURCE_DIR}/*.qrc 
    ${CMAKE_CURRENT_SOURCE_DIR}/*.svg 
    ${CMAKE_CURRENT_SOURCE_DIR}/*.ui 
    )

foreach(File ${Files})
    get_filename_component(BaseName ${File} NAME)
    configure_file(${File} ${CMAKE_BINARY_DIR}/${BaseName} COPYONLY)
endforeach()

add_custom_command( OUTPUT commit_msg_ui.py 
    COMMAND pyuic4 -o commit_msg_ui.py commit_msg.ui
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/commit_msg.ui )

add_custom_target(qgis_plugin ALL DEPENDS commit_msg_ui.py ${Files})

add_subdirectory(test)
