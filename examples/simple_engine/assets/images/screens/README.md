# screens/

Title-screen and ending-screen art, copied over from the main project.
**Not used by the demo** -- there is currently only one `Scene`
(`PlayScene`), so the game jumps straight into gameplay with no menu or
game-over screen.

This is the natural next milestone once you're comfortable with
`PlayScene`: write a `TitleScene(Scene)` that draws `Title ScreenText.png`
and waits for a keypress before `Game` switches to `PlayScene`, and an
`EndingScene(Scene)` that draws `EndingScreen.png` when all enemies are
destroyed. See "Chapter 6 -- Where To Go Next" in the PDF guide.
