# Curate Perceptual Learning Offline Implementation
version: 16-12-21
## How to run the code
Run the main file (curate_pl_offline.py) in PsychoPy. 

## What will happen?
1. Key in your ID.
2. Instructions page (press `Enter` or `Return` to proceed)
3. There will one warm up trial. 
4. The followings are the experiment trials. 
   1. The number of trials are based on the number sessions you have had.
   2. The updating of difficulty of rotation and noise is based on:  
      1. 3D1U for the first 2 sessions with isolated difficulty
      2. Fixed, where the Low (Difficulty in previous session - 6), Medium(Difficulty in previous session), and High (Difficulty in previous session + 6).
5. In each trial, the experimentee must either click `left` for anti-clockwise or `right` for clockwise.
6. The program wil save the trial results into a csv file (starting with your ID).
7. The program will only save the profile of experimentee at the end as a .pickle file.