// Copyright (C) 2023 NGITL
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15


import "./items"

Window {
    id: window

    width: 800
    height: 600

    property int entry_width: 220

    property color background_color: '#272537'
    property color accent_color: "#6e509e"
    property color foreground_color: '#333143'

    property color lightFontColor: '#F4EEE0' // off-white for text behind a light background

    color: background_color
    minimumWidth: 800
    minimumHeight: 600
    visible: true
    title: qsTr("Database Interface")

    Rectangle {
        id: fill_rect
        width: parent.width
        height: 130
//        color: window.accent_color
        color: "transparent"

//        color: "red"

        TitleBar {
               id: titleBar
               width: parent.width
               height: parent.height-filler_rect.height-command.height
        }
        Rectangle{
            id: filler_rect
            width: parent.width
            height: 6
            y: titleBar.height
            color: window.accent_color
//            color: "transparent"
        }

        Rectangle{

            id: command

            width: parent.width
//            height: parent.height* 0.45 - filler_rect.height
            height: 50
            y: titleBar.height + filler_rect.height
            color: window.foreground_color

            Rectangle {
                id: connection_status_rect
                width: 100
                height: parent.height* 0.7
                x: 5
                anchors.verticalCenter: parent.verticalCenter
                color: "transparent"
                Text {
                    text: qsTr("Connection")
                    color: lightFontColor
                    anchors.top: parent.top
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                CuSwitch{
                    oncolor: accent_color
                    width: parent.width * 0.8
                    height: parent.height *0.6
                    anchors.bottom: parent.bottom
                    anchors.horizontalCenter: parent.horizontalCenter
                    textColor: '#3B3730'

                    switchOn: database.connection_status

                    MouseArea{
                        anchors.fill: parent
                        onClicked: {
                            database.retryConnection()
                        }
                    }
                }
            }

            CuButton {
                id: update_button
                buttonText: "Update"
                width: 100
                height: parent.height* 0.7
                anchors.leftMargin: 5
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: connection_status_rect.right

                onClicked: database.requestFromDatabase("get_data")
            }

            CuButton {
                id: refresh_button
                buttonText: "Refresh"
                width: 100
                height: parent.height* 0.7
                anchors.leftMargin: 5
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: update_button.right

                onClicked: database.requestFromDatabase("refresh")
            }

            CuButton {
                id: reconnect_button
                buttonText: "Reconnect"
                width: 100
                height: parent.height* 0.7
                anchors.leftMargin: 5
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: refresh_button.right

                onClicked: database.requestFromDatabase("reconnect")
            }
            CuButton {
                buttonText: "Save Unsent"
                width: 100
                height: parent.height* 0.7
                anchors.rightMargin: 5
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
            }

            ComboBox {
                id: shown_data
                width: 150
                height: parent.height*0.7
                anchors.leftMargin: 5
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: reconnect_button.right
                model: database.available_data_entries

                onCurrentTextChanged: {
                    database.changeShownData(currentText);
                    data_window.updateTotalWidth();
                }
            }
         }
    }
    Rectangle{
        id: filler_rect_2
        width: parent.width
        height: 6
        anchors.top: fill_rect.bottom
//        color: window.accent_color
        color: "transparent"
    }
    Rectangle{
        id: database_info
        width: parent.width*0.2
        height: data_window.height
        color: foreground_color
        anchors.bottom: parent.bottom

        Rectangle{
            id: data_internet_connection
            width: parent.width * 0.9
            height: parent.height - anchors.topMargin * 2
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: (parent.width - data_internet_connection.width)/2
            color: "transparent"
            border.width: 2
            border.color: accent_color
            radius: 5

        }
    }

    DataWindow{
        id: data_window
        databaseModel: database
        width: window.width - database_info.width - 6
        height: window.height - fill_rect.height - filler_rect_2.height
        anchors.right: parent.right

    }




}
