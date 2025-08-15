document.addEventListener("DOMContentLoaded", () => {
  // --- UI Elements ---
  const recordBtn = document.getElementById("recordBtn");
  const statusDisplay = document.getElementById("statusDisplay");
  const audioPlayer = document.getElementById("audioPlayer");
  const transcriptBox = document.getElementById("transcriptBox");

  // --- SVG Icons ---
  const icons = {
    mic: `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24"><path d="M12 14c1.66 0 2.99-1.34 2.99-3L15 5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.49 6-3.31 6-6.72h-1.7z"/></svg>`,
    stop: `<svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24"><path d="M6 6h12v12H6z"/></svg>`,
    thinking: `<div class="spinner"></div>`, // A simple CSS spinner
  };

  // --- Application State ---
  let appState = "idle"; // idle, recording, thinking, speaking
  let mediaRecorder = null;
  let recordedChunks = [];
  let sessionId = null;

  // --- Functions ---

  /**
   * Updates the UI based on the current application state.
   */
  const updateUI = () => {
    switch (appState) {
      case "idle":
        recordBtn.innerHTML = icons.mic;
        recordBtn.disabled = false;
        recordBtn.classList.remove("recording");
        statusDisplay.textContent = "Tap the mic to speak";
        break;
      case "recording":
        recordBtn.innerHTML = icons.stop;
        recordBtn.disabled = false;
        recordBtn.classList.add("recording");
        statusDisplay.textContent = "Listening...";
        break;
      case "thinking":
        recordBtn.innerHTML = icons.thinking;
        recordBtn.disabled = true;
        recordBtn.classList.remove("recording");
        statusDisplay.textContent = "Thinking...";
        break;
      case "speaking":
        recordBtn.innerHTML = icons.mic;
        recordBtn.disabled = true;
        statusDisplay.textContent = "Speaking...";
        break;
    }
  };

  /**
   * Initializes the application and sets up the session.
   */
  const initialize = () => {
    const urlParams = new URLSearchParams(window.location.search);
    sessionId = urlParams.get("session_id");
    if (!sessionId) {
      sessionId = crypto.randomUUID();
      window.history.replaceState({}, "", `?session_id=${sessionId}`);
    }
    console.log("Session ID:", sessionId);
    updateUI(); // Set initial UI state
  };

  /**
   * Handles the main interaction with the record button.
   */
  const handleRecordButtonClick = () => {
    if (appState === "idle" || appState === "speaking") {
      startRecording();
    } else if (appState === "recording") {
      stopRecording();
    }
  };

  /**
   * Starts the audio recording process.
   */
  const startRecording = async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      statusDisplay.textContent = "Audio recording is not supported.";
      return;
    }
    appState = "recording";
    updateUI();
    recordedChunks = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) recordedChunks.push(event.data);
      };
      mediaRecorder.onstop = processAudio;
      mediaRecorder.start();
    } catch (err) {
      console.error("Microphone access error:", err);
      statusDisplay.textContent = "Please allow microphone access.";
      appState = "idle";
      updateUI();
    }
  };

  /**
   * Stops the audio recording.
   */
  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
      mediaRecorder.stop();
    }
  };

  /**
   * Processes the recorded audio and sends it to the server.
   */
  const processAudio = async () => {
    // --- FIX: Check if any audio was actually recorded ---
    if (recordedChunks.length === 0) {
      console.log("No audio recorded.");
      statusDisplay.textContent = "No audio recorded. Please try again.";
      appState = "idle";
      updateUI();
      return; // Exit the function to prevent sending an empty file
    }

    appState = "thinking";
    updateUI();
    const audioBlob = new Blob(recordedChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio_file", audioBlob, "user_audio.webm");

    try {
      const response = await fetch(`/agent/chat/${sessionId}`, {
        method: "POST",
        body: formData,
      });

      if (response.headers.get("X-Error") === "true") {
        throw new Error("Sorry, I'm having trouble connecting right now.");
      }
      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const result = await response.json();
      if (result.audio_url) {
        playAgentResponse(result.audio_url, result.text);
      } else {
        throw new Error("Did not receive a valid audio response.");
      }
    } catch (error) {
      console.error("Error during agent chat:", error);
      transcriptBox.textContent = error.message;
      transcriptBox.hidden = false;
      appState = "idle";
      updateUI();
    }
  };

  /**
   * Plays the agent's audio response.
   * @param {string} audioUrl - The URL of the audio to play.
   * @param {string} text - The transcript of the agent's response.
   */
  const playAgentResponse = (audioUrl, text) => {
    appState = "speaking";
    updateUI();
    transcriptBox.textContent = text;
    transcriptBox.hidden = false;
    audioPlayer.src = audioUrl;
    audioPlayer.play();
  };

  // --- Event Listeners ---
  recordBtn.addEventListener("click", handleRecordButtonClick);

  audioPlayer.onended = () => {
    // After speaking, go back to idle, ready for the user to tap again.
    appState = "idle";
    updateUI();
  };

  // --- Initial Load ---
  initialize();
});
