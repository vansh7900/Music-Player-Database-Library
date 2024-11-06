-- Step 1: Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS music_player;

-- Step 2: Use the music_player database
USE music_player;

-- Step 3: Create the songs table if it doesn't already exist
CREATE TABLE IF NOT EXISTS songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    path VARCHAR(255) NOT NULL
);

-- Step 4: (Optional) Insert some example data
INSERT INTO songs (name, path)
VALUES
('Millionaire.mp3', '\C:\Users\vansh\Downloads\song'),
('Lemonade.mp3', '\C:\Users\vansh\Downloads\song'),
('White_Brown.mp3', '\C:\Users\vansh\Downloads\song'),
('OnTop.mp3', '\C:\Users\vansh\Downloads\song'),
('Admirin.mp3', '\C:\Users\vansh\Downloads\song'),
('WinningSpeech.mp3', '\C:\Users\vansh\Downloads\song');

-- Step 5: (Optional) Query to check the inserted songs
SELECT * FROM songs;
