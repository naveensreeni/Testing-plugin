import asyncio
from playwright.async_api import async_playwright, expect
import os
import pytest

@pytest.mark.asyncio
async def test_snake_game():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('snake.html')
        await page.goto(f'file://{file_path}')

        # Verify initial state
        score = page.locator("#score")
        await expect(score).to_have_text("Score: 0")

        overlay_text = page.locator("#overlay-text")
        await expect(overlay_text).to_have_text("Press Any Arrow Key to Start")

        overlay = page.locator("#overlay")
        await expect(overlay).to_be_visible()

        # Start the game
        await page.press("body", "ArrowUp")

        # Verify game has started
        await expect(overlay).to_be_hidden()

        # Cause a game over by hitting the wall.
        # The snake starts at (10,10) on a 20x20 grid. Moving up 11 times will hit the wall.
        for _ in range(11):
            await page.press("body", "ArrowUp")
            # Wait for the game loop to process the move. The interval is 100ms in the game.
            await page.wait_for_timeout(110)

        # Verify game over screen
        await expect(overlay).to_be_visible()
        await expect(overlay_text).to_have_text("Game Over")

        # The score should still be 0 as no food was eaten.
        await expect(score).to_have_text("Score: 0")

        # Restart the game
        restart_button = page.locator("#restartBtn")
        await restart_button.click()

        # Verify game has reset
        await expect(score).to_have_text("Score: 0")
        await expect(overlay_text).to_have_text("Press Any Arrow Key to Start")
        await expect(overlay).to_be_visible()

        await browser.close()
