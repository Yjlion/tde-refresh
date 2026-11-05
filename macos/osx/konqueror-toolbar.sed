# Trim Konqueror's main toolbar to back/forward/up and the view-mode buttons.
/<ToolBar[^>]*name="mainToolBar"/,/<\/ToolBar>/{
	/name="home"/d
	/name="reload"/d
	/name="stop"/d
	/name="print"/d
	/name="animated_logo"/d
	/<Separator\/>/d
	/name="fullscreen"/d
}
