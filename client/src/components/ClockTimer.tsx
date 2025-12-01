import { useEffect, useState } from "react";
import { Play, Pause, RotateCcw, X, Timer, BellRing } from 'lucide-react';

export default function ClockTimer() {
    //user input states
    const[inputMinutes, setInputMinutes] = useState<number>(0);
    const[inputSeconds, setInputSeconds] = useState<number>(10);
    
    //state for timer logic
    const[timeLeft, setTimeLeft] = useState<number>(10);
    const[initialTime, setInitialTime] = useState<number>(10);
    const[isActive, setIsActive] = useState<boolean>(false);
    const[isPaused, setIsPaused] = useState<boolean>(false); 

    //state for "Alert" modal
    const[showActiveModal, setShowActiveModal] = useState<boolean>(false);
    

    //Timer Logic Here
    useEffect(() => {
        let interval:ReturnType<typeof setInterval>|null =null;
        if(isActive && !isPaused && timeLeft >0){
            interval = setInterval(() => {
                setTimeLeft((timeLeft) => timeLeft -1);
            }, 1000);
        } else if(timeLeft === 0 && isActive){
            if(interval !== null) clearInterval(interval);
            setIsActive(false);
            setShowActiveModal(true);
        }
        return () => {
            if(interval !== null) clearInterval(interval);
        };
    },[isActive, isPaused, timeLeft]);

    //Handler Functions
    const handleStart = () =>{
        if(isActive && isPaused)
        {
            setIsPaused(false);
            return;
        }
        const totalSeconds = (inputMinutes*60)+inputSeconds;
        if(totalSeconds <=0) return;

        setInitialTime(totalSeconds);
        setTimeLeft(totalSeconds);
        setIsActive(true);
        setIsPaused(false);
        setShowActiveModal(false);
    };
    const handlePause = () =>{
        setIsPaused(true);
    }

    const handleReset = () =>{
        setIsActive(false);
        setIsPaused(false);
        setTimeLeft(0);
        setShowActiveModal(false);
    }
    const handleCloseModal = () =>{
        setShowActiveModal(false);
    }
    
    const handleInputChange = (
        e : React.ChangeEvent<HTMLInputElement>,
        setter : React.Dispatch<React.SetStateAction<number>>
    )=>{
        const val = parseInt(e.target.value);
        setter(isNaN(val)?0:Math.max(0, val ));
    };

    const formatTime = (seconds :number) : string =>{
        const m = Math.floor(seconds/60);
        const s  = seconds % 60;
        return `${m.toString().padStart(2,'0')}:${s.toString().padStart(2,'0')}`;
    }

    const radius = 80;
    const circumference = 2 * Math.PI * radius;
    const progress = initialTime ? (timeLeft / initialTime) : 0;
    const strokeDashoffset = circumference * (1 - progress);    
    return (
            <div>
      {/* Header */}
      <div>
        {/* Circular Display */}
        {/* Inline styles retained ONLY for SVG geometry/rotation logic */}
        <div style={{ position: 'relative', width: '256px', height: '256px' }}>
          <svg width="256" height="256" style={{ transform: 'rotate(-90deg)' }}>
            {/* Background Circle */}
            <circle
              cx="128"
              cy="128"
              r={radius}
              stroke="lightgray"
              strokeWidth="8"
              fill="transparent"
            />
            {/* Progress Circle */}
            <circle
              cx="128"
              cy="128"
              r={radius}
              stroke="blue"
              strokeWidth="8"
              fill="transparent"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
            />
          </svg>
          
          {/* Digital Time Display */}
          <div style={{ position: 'absolute', top: '45%', left: '0', right: '0', textAlign: 'center' }}>
            <h2>
              {isActive || timeLeft > 0 ? formatTime(timeLeft) : formatTime((inputMinutes * 60) + inputSeconds)}
            </h2>
          </div>
        </div>

        {/* Configuration Inputs */}
        {!isActive && (
          <div>
            <div>
              <label>Minutes</label>
              <input
                type="number"
                min="0"
                max="59"
                value={inputMinutes}
                onChange={(e) => handleInputChange(e, setInputMinutes)}
              />
            </div>
            <span>:</span>
            <div>
              <label>Seconds</label>
              <input
                type="number"
                min="0"
                max="59"
                value={inputSeconds}
                onChange={(e) => handleInputChange(e, setInputSeconds)}
              />
            </div>
          </div>
        )}

        {/* Controls */}
        <div>
          {!isActive ? (
            <button onClick={handleStart}>
              <Play size={16} /> START
            </button>
          ) : (
            <>
              {isPaused ? (
                <button onClick={handleStart}>
                  <Play size={16} /> RESUME
                </button>
              ) : (
                <button onClick={handlePause}>
                  <Pause size={16} /> PAUSE
                </button>
              )}
              
              <button onClick={handleReset}>
                <RotateCcw size={16} /> RESET
              </button>
            </>
          )}
        </div>
      </div>

      {/* The Alert Section */}
      {showActiveModal && (
        <div style={{ border: '1px solid black', padding: '20px', marginTop: '20px' }}>
          <div>
            <BellRing />
          </div>
          
          <h2>Time's Up!</h2>
          <p>
            Your timer for <strong>{formatTime(initialTime)}</strong> has finished.
          </p>
          
          <button onClick={handleCloseModal}>
            <X size={16} /> Dismiss
          </button>
        </div>
      )}
    </div>
  );
}
