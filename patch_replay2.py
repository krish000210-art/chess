import re

with open('index.html', 'r') as f:
    content = f.read()

replay_js = """        let replayTimer = null;
        let replayMoves = [];
        let replayIndex = 0;

        function reviewMatch() {
            document.getElementById('gameover-overlay').classList.add('hidden');
            state.gameMode = 'analysis';
            state.isAnalysisEnabled = true;

            // Get all moves from the game
            const history = state.game.history();
            // Take the last 25 moves
            const startHistory = history.length > 25 ? history.slice(0, history.length - 25) : [];
            replayMoves = history.length > 25 ? history.slice(history.length - 25) : history;

            // Reset the game to the point before the last 25 moves
            const replayGame = new Chess();
            try { replayGame.load(state.initialFenRef); } catch(e) {}
            startHistory.forEach(m => replayGame.move(m));

            state.game = replayGame;
            state.fenInput = state.game.fen();
            updateUI();
            renderBoard();

            // Start replay
            replayIndex = 0;
            clearInterval(replayTimer);
            replayTimer = setInterval(() => {
                if (replayIndex < replayMoves.length) {
                    const move = state.game.move(replayMoves[replayIndex]);
                    if (move) playMoveSound(state.game, move);
                    state.fenInput = state.game.fen();
                    renderBoard();
                    updateUI();
                    triggerEval();
                    replayIndex++;
                } else {
                    clearInterval(replayTimer);
                }
            }, 1000);
        }"""

# Manually find and replace to ensure it hits
old_str = """                function reviewMatch() {
            document.getElementById('gameover-overlay').classList.add('hidden');
            state.gameMode = 'analysis';
            state.isAnalysisEnabled = true;
            // Provide a starting point for analysis by setting the fen input correctly
            state.fenInput = state.game.fen();
            // Undo history will still be intact because we haven't created a new Chess instance.
            // The user can now use the back/forward buttons or 'undo' to step through the past moves.
            updateUI();
            triggerEval();
            renderBoard();
        }"""

content = content.replace(old_str, replay_js)

with open('index.html', 'w') as f:
    f.write(content)
