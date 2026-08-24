# The One Where We Make Cups

## Console Version

Run ```pyclasses.py``` from the console to play the console version of the game. 

## Structure
```
cups-game/
  backend/
    app/
      __init__.py
      main.py
      game/
        __init__.py
        models.py
        rules.py
        engine.py
    requirements.txt
  frontend/
    index.html
    package.json
    vite.config.js
    src/
      main.jsx
      App.jsx
      api.js
      styles.css
      components/
        MainMenu.jsx
        GameTable.jsx
        CardView.jsx
        HandView.jsx
        Controls.jsx
        EventLog.jsx
```

### Media Structure

```
frontend/public/assets/
  images/
    background.jpg
    card-back.png
    deck-back.png
  sounds/
    menu-music.mp3
    gameplay-music.mp3
    deal.mp3
    discard.mp3
    payout.mp3
```


## Run Locally

Backend
```
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend
```
cd frontend
npm install
npm run dev
```

