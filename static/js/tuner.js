/**
 * Guitar Tuner Web Application
 * Audio synthesizer engine using Web Audio API
 */

// Audio Context and Synthesizer State
let audioCtx = null;
let currentOscillator = null;
let currentGainNode = null;
let isPlaying = false;

// Selected String State
let activeString = {
    number: 6,
    note: "E",
    octave: 2,
    frequency: 82.41
};

// DOM Elements
const selectedNoteEl = document.getElementById("selectedNote");
const selectedOctaveEl = document.getElementById("selectedOctave");
const currentFrequencyEl = document.getElementById("currentFrequency");
const tunerNeedleEl = document.getElementById("tunerNeedle");
const playbackStatusEl = document.getElementById("playbackStatus");
const toggleSoundBtn = document.getElementById("toggleSoundBtn");
const toggleSoundText = document.getElementById("toggleSoundText");
const stopSoundBtn = document.getElementById("stopSoundBtn");
const waveformSelect = document.getElementById("waveformSelect");
const stringButtons = document.querySelectorAll(".string-card");

/**
 * Initialize or get Web Audio Context
 */
function getAudioContext() {
    if (!audioCtx) {
        const AudioContextClass = window.AudioContext || window.webkitAudioContext;
        audioCtx = new AudioContextClass();
    }
    if (audioCtx.state === "suspended") {
        audioCtx.resume();
    }
    return audioCtx;
}

/**
 * Play synthesizer reference pitch for the current active string
 */
function playTone(freq) {
    stopTone();

    const ctx = getAudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = waveformSelect.value || "triangle";
    osc.frequency.setValueAtTime(freq, ctx.currentTime);

    // Audio envelope: smooth attack to prevent click/pop
    gain.gain.setValueAtTime(0.0001, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.3, ctx.currentTime + 0.05);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();

    currentOscillator = osc;
    currentGainNode = gain;
    isPlaying = true;

    // Update UI status
    playbackStatusEl.classList.add("playing");
    playbackStatusEl.innerHTML = `<span class="pulse-indicator"></span> Sounding ${activeString.note}${activeString.octave} (${freq} Hz)`;
    toggleSoundText.textContent = "Stop Tone";
    tunerNeedleEl.classList.add("in-tune");
    tunerNeedleEl.style.left = "50%";

    // Highlight vibrating string wire
    highlightVibration(activeString.number, true);
}

/**
 * Stop currently sounding reference tone
 */
function stopTone() {
    if (currentGainNode && audioCtx) {
        // Smooth fade out release
        try {
            currentGainNode.gain.cancelScheduledValues(audioCtx.currentTime);
            currentGainNode.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.04);
            setTimeout(() => {
                if (currentOscillator) {
                    currentOscillator.stop();
                    currentOscillator.disconnect();
                    currentOscillator = null;
                }
            }, 50);
        } catch (e) {
            console.error("Audio stop error", e);
        }
    }

    isPlaying = false;
    playbackStatusEl.classList.remove("playing");
    playbackStatusEl.innerHTML = `<span class="pulse-indicator"></span> Click a string to hear the pitch`;
    toggleSoundText.textContent = "Play Tone";
    tunerNeedleEl.classList.remove("in-tune");

    // Clear all vibrations
    document.querySelectorAll(".vibrating-line").forEach(line => line.classList.remove("vibrating"));
}

/**
 * Highlight vibrating string line on virtual fretboard
 */
function highlightVibration(stringNumber, active) {
    document.querySelectorAll(".vibrating-line").forEach(line => line.classList.remove("vibrating"));
    const targetLine = document.getElementById(`vibeLine${stringNumber}`);
    if (targetLine && active) {
        targetLine.classList.add("vibrating");
    }
}

/**
 * Select a string and update display
 */
function selectString(btn) {
    stringButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");

    const number = parseInt(btn.dataset.string, 10);
    const note = btn.dataset.note;
    const octave = btn.dataset.octave;
    const freq = parseFloat(btn.dataset.freq);

    activeString = { number, note, octave, frequency: freq };

    // Update Hero Display
    selectedNoteEl.textContent = note;
    selectedOctaveEl.textContent = octave;
    currentFrequencyEl.textContent = freq.toFixed(2);

    // Subtle needle bounce to simulate detection
    tunerNeedleEl.style.left = "48%";
    setTimeout(() => {
        tunerNeedleEl.style.left = "50%";
    }, 150);

    // Play tone automatically upon string selection
    playTone(freq);
}

// Event Listeners for String Cards
stringButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        selectString(btn);
    });
});

// Toggle Sound Button
toggleSoundBtn.addEventListener("click", () => {
    if (isPlaying) {
        stopTone();
    } else {
        playTone(activeString.frequency);
    }
});

// Stop Sound Button
stopSoundBtn.addEventListener("click", () => {
    stopTone();
});

// Change Waveform
waveformSelect.addEventListener("change", () => {
    if (isPlaying) {
        playTone(activeString.frequency);
    }
});

// Keyboard Shortcuts: Keys 1 to 6 select string, Space toggles audio
window.addEventListener("keydown", (e) => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "SELECT") return;

    if (e.key >= "1" && e.key <= "6") {
        const targetBtn = document.getElementById(`stringBtn${e.key}`);
        if (targetBtn) {
            selectString(targetBtn);
        }
    } else if (e.code === "Space") {
        e.preventDefault();
        if (isPlaying) {
            stopTone();
        } else {
            playTone(activeString.frequency);
        }
    }
});

console.log("Guitar Tuner initialized. CI/CD Ready.");
