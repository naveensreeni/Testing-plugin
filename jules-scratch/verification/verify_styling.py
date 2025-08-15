import asyncio
from playwright.async_api import async_playwright, expect
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('snake.html')
        url = f'file://{file_path}'
        print(f"Navigating to: {url}")

        # Go to the local HTML file
        await page.goto(url)

        # Wait for the body to have the correct background color
        await expect(page.locator('body')).to_have_css('background-color', 'rgb(26, 32, 44)')
        await page.wait_for_timeout(1000) # 1 second delay

        # 1. Take a screenshot of the initial login screen
        await page.screenshot(path="jules-scratch/verification/01_login_screen_local_css.png")

        # 2. Enter a name and start the game
        await page.get_by_placeholder("Player").fill("Jules")
        await page.get_by_role("button", name="Start Game").click()

        # 3. Wait for the player name to be displayed
        player_name_display = page.locator("#playerNameDisplay")
        await expect(player_name_display).to_have_text("Player: Jules")
        await page.wait_for_timeout(1000) # 1 second delay

        # 4. Take a screenshot of the game screen with the player's name
        await page.screenshot(path="jules-scratch/verification/02_game_screen_local_css.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
