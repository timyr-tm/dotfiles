import Quickshell

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import "./"
import "./modules/workspaces"

PanelWindow {
    color: "transparent"
    implicitHeight: Config.height

    anchors {
        top: true
        left: true
        right: true
    }

    margins {
        top: Config.gaps_out
        bottom: Config.gaps_in
        left: Config.gaps_out
        right: Config.gaps_out
    }

    RowLayout {
        anchors.fill: parent

        Control {
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignLeft

            contentItem: RowLayout {
                WorkspacesModule {
                    Layout.alignment: Qt.AlignVCenter
                }
            }

            background: Rectangle {
                color: "transparent"
                border {
                    width: Config.border.width
                    color: Config.border.color
                }
            }
        }
    }
}
