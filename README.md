# BetterDino
- BetterDino game is inspired by the dino game we see when we receive no internet connection on our browser like chrome.
- Our reference is from maxontech who created his replica of the dino game using pygame. His youtube videos and github can be seen from the link below:
    - https://youtube.com/playlist?list=PL30AETbxgR-fAbwiuU1vDl3owNUPUuVrz&si=_g38aaVXZGXDdXaI
    - https://github.com/maxontech/chrome-dinosaur.git
- This project focuses on modifying and adding features to the preexisting game in the hopes of making it "better".
- The tools used to assist this project include: Github and GIMP

## Game Inforamtion:
### Main
- Main is where the game instance is being played.
- The objective of the game is to survive as the dino as long as possible.
- On the game instance includes: Obstacles, Dino, Projectiles, Clouds, and Background
- The dino has 3 hearts.
    - When a dino gets hit it, it reduces the heart of the dino by 1 and there is a small time frame where the dino is immune from getting hit.
    - Once the dino is hit the 3rd time, it has no hearts left so the dino is considered dead and its game over.
- The game increases in speed determined by game speed which increments by 1 for every determined level length (example: each time points modulus 100 points is passed, the game speed increases by 1)
### Player actions:
- NOTE: in this version of the game players can perform actions with no cooldown.
1. Press `W` or `Up` key to jump (hold jump to reach its maximum; release `W` to go down faster)
2. Press `S` or `Down` key to crouch.
3. Press `Left click` to shoot projectile one time towards where your mouse clicked in the area.
    - Projectile moves based from the dino's position and to the position where your mouse clicked in a straight line.
4. Press `Esc` to pause the game.
    - Press `R` to resume the game instance; There will be a 3 second countdown after the `R` key is pressed.
    - Press `Q` to quit the game instance and go to menu.
5. Press `A` key to toggle aim helper which is a red line that is shown from the dino to your mouse cursor.
6. On default the dino runs standing tall on the ground.
### Obstacles:
- NOTE: in this version of the game obstacles only appear 1 at a time; in the future obstacles should be have more variety such as a preset of attacks.
- These obstacles include: small cactus, large cactus, pterodactylus, and tumbleweed.
- All obstacles move from right to left appearing from the right to left based on game speed.
- Tumbleweed is slightly different since it moves in the y axis as well like a parabola.
### Menu
- Menu is mainly used as a place for user to see current score, high score, and death counts (NOTE: could be changed in different version).
- Press `any` keyboard key to start.
- When first initialized all the stats would be 0.

## To do:
- [x] Add ability to pause the game where player still able to see the screen, the screen is grey, pause icon.
- [x] Create a better menu/start screen.
- [ ] Add a boss; boss is trigerred after player reaches certain condition (for example: reaches 2000 points).
- [ ] Create better hitbox for the sprites
- [ ] Create user save file
- [x] Replace the dino's ability to destroy tumbleweed by clicking to shooting fireballs and when it hits it, the tumbleweed gets burnt
- [x] Create projectile
- [x] Add the ability of using W and S equivalent to Up key and Down key respectively.
- [x] Add lives for the dino
- [x] Set death animation
- [x] Add sound effects
- [x] Make game more responsive to user's action with sound or other effects.
## Reference:
- https://youtube.com/playlist?list=PL30AETbxgR-fAbwiuU1vDl3owNUPUuVrz&si=_g38aaVXZGXDdXaI
- https://www.youtube.com/watch?v=tJiKYMQJnYg