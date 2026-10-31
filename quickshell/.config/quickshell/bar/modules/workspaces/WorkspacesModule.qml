import Quickshell.Hyprland

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../../"

RowLayout {
    spacing: 0
    Layout.leftMargin: 5
    Layout.rightMargin: 5
    Repeater {
        model: Hyprland.workspaces.values
        delegate: AbstractButton {
            required property HyprlandWorkspace modelData

            Layout.fillHeight: true

            leftPadding: 10
            rightPadding: 10

            onClicked: modelData.activate()

            contentItem: Label {
                text: modelData.name
                color: Config.modules.font.color
                verticalAlignment: Text.AlignVCenter

                font {
                    family: Config.modules.font.family
                    pixelSize: Config.modules.font.size
                    underline: modelData.active
                    bold: modelData.active
                }
            }
        }
    }

    Component.onCompleted: console.log(Object.keys(Hyprland))
}
