pragma Singleton

import QtQuick

QtObject {
    readonly property int height: 32
    readonly property int gaps_out: 10
    readonly property int gaps_in: 5

    readonly property QtObject border: QtObject {
        readonly property color color: "#89b4fa"
        readonly property real width: 2
    }

    readonly property QtObject modules: QtObject {
        readonly property QtObject font: QtObject {
            readonly property string family: "Fira Code"
            readonly property int size: 16
            readonly property color color: "#cdd6f4"
        }

        readonly property QtObject workspaces: QtObject {

        }
    }
}
