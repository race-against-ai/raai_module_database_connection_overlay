// Copyright (C) 2023 NGITL
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15


import "./items"

Window {
    id: window

    width: 800
    height: 600

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
        height: parent.height/4.5
//        color: window.accent_color
        color: "transparent"

//        color: "red"

        TitleBar {
               id: titleBar
               width: parent.width
               height: parent.height*0.55
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
            height: parent.height* 0.45 - filler_rect.height
            y: titleBar.height + filler_rect.height
//            color: window.foreground_color
            color: "red"

            CuButton {
                buttonText: "Connect"

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

    Flickable {
        id: flickableData
        width: parent.width
        height: parent.height - fill_rect.height
        contentWidth: rowOfTexts.width
        contentHeight: data_rect.height
        anchors.top: filler_rect_2.bottom

        clip: true

        Rectangle{
            id: data_rect
            color: "transparent"
            width: parent.parent.width
            height: parent.parent.height - fill_rect.height

            Rectangle {
                id: data_keys
                width: parent.width
                height: parent.height * 0.08
                anchors.top: parent.top
                color: foreground_color

                Row {
                    id: rowOfTexts
                    spacing: 5 // Adjust spacing as needed
                    anchors.fill: parent
                    property int totalWidth: 0 // Initialize totalWidth

                    Repeater {
                        model: database.database_keys
                        delegate: Item {
                            width: 150
                            height: parent.height

                            Text {
                                text: modelData.key
                                anchors.centerIn: parent
                                color: lightFontColor
                            }

                            // Add the width of each key to totalWidth
                            Component.onCompleted: {
                                rowOfTexts.totalWidth += width
                            }
                        }
                    }
                }
            }

            Rectangle {
                width: parent.width
                height: parent.height - data_keys.height - 6
                anchors.bottom: parent.bottom
                color: "transparent"
                ScrollView {
                    id: scrollView
                    anchors.fill: parent
                    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                    ScrollBar.vertical: ScrollBar{
                        id: scrollBar

                        hoverEnabled: true
                        policy: ScrollBar.AsNeeded
                        width: 6

                        parent: scrollView.parent
                        x: scrollView.mirrored ? 0 : scrollView.width - width
                        height: scrollView.availableHeight

                        background: Rectangle {
                            color: foreground_color
                        }
                    }

                    Column {
                        id: column
                        anchors.fill: parent
                        spacing: 3

                        Repeater {
                            id: data_repeater
                            model: database.data

                            delegate: DataEntry {
                                width: window.width-4
                            }
                        }
                    }
                }
            }
        }
        ScrollBar.horizontal: ScrollBar {
            width: 6
            policy: ScrollBar.AsNeeded
        }
    }


}
