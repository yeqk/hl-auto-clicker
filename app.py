import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

from models import Sequence, ClickEvent
from recorder import Recorder
from player import Player
from humanizer import Humanizer
from hotkeys import HotkeyManager

# Set application appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AutoClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎯 HL Auto Clicker")
        self.geometry("640x850")
        self.resizable(False, False)

        # Core logic variables
        self.sequence = Sequence()
        self.humanizer = Humanizer(timing_variance=0.15, position_jitter=3, pause_chance=0.02)
        
        # Engines
        # Use lambda wrapper to safely run on UI main thread context
        self.recorder = Recorder(on_event_callback=self._safe_on_record_event)
        self.player = Player(
            humanizer=self.humanizer, 
            on_loop_complete=self._safe_on_loop_complete,
            on_stopped=self._safe_on_playback_stopped
        )
        self.hotkeys = HotkeyManager(
            on_record_toggle=self.toggle_recording,
            on_play_toggle=self.toggle_playback,
            on_stop_all=self.stop_all
        )
        
        # Initialize hotkeys
        self.hotkeys.start()

        # Build GUI Layout
        self._build_ui()
        self._update_ui_state()

        # Clean exit hook
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _build_ui(self):
        # ---------------- Title / Header ----------------
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        title_lbl = ctk.CTkLabel(
            title_frame, 
            text="🎯 HL Auto Clicker", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold")
        )
        title_lbl.pack(side="left")

        # Always on Top switch
        self.always_on_top_switch = ctk.CTkSwitch(
            title_frame, 
            text="Always on Top", 
            command=self._toggle_always_on_top,
            font=ctk.CTkFont(family="Inter", size=12)
        )
        self.always_on_top_switch.pack(side="right", pady=5)

        # ---------------- Quick Control Panel ----------------
        ctrl_frame = ctk.CTkFrame(self, corner_radius=12)
        ctrl_frame.pack(fill="x", padx=20, pady=10)
        ctrl_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Action buttons
        self.record_btn = ctk.CTkButton(
            ctrl_frame, 
            text="● Record", 
            fg_color="#2ecc71", 
            hover_color="#27ae60",
            text_color="black",
            font=ctk.CTkFont(weight="bold"),
            command=self.toggle_recording
        )
        self.record_btn.grid(row=0, column=0, padx=8, pady=10, sticky="ew")

        self.play_btn = ctk.CTkButton(
            ctrl_frame, 
            text="▶ Play Loop", 
            fg_color="#3498db", 
            hover_color="#2980b9",
            text_color="white",
            font=ctk.CTkFont(weight="bold"),
            command=self.toggle_playback
        )
        self.play_btn.grid(row=0, column=1, padx=8, pady=10, sticky="ew")

        self.clear_btn = ctk.CTkButton(
            ctrl_frame, 
            text="🗑 Clear", 
            fg_color="#7f8c8d", 
            hover_color="#95a5a6",
            text_color="white",
            command=self.clear_sequence
        )
        self.clear_btn.grid(row=0, column=2, padx=8, pady=10, sticky="ew")

        # ---------------- Real-time Event Feed ----------------
        list_frame = ctk.CTkFrame(self, corner_radius=12)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(2, weight=1)

        list_title = ctk.CTkLabel(
            list_frame, 
            text="Recorded Click Sequence", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        list_title.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")

        # Table Header labels
        tbl_header = ctk.CTkFrame(list_frame, fg_color="transparent")
        tbl_header.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 2))
        
        ctk.CTkLabel(tbl_header, text="Index", width=50, anchor="w", text_color="gray").pack(side="left")
        ctk.CTkLabel(tbl_header, text="Action Type", width=120, anchor="w", text_color="gray").pack(side="left")
        ctk.CTkLabel(tbl_header, text="Coordinates", width=150, anchor="w", text_color="gray").pack(side="left")
        ctk.CTkLabel(tbl_header, text="Delay (seconds)", width=100, anchor="e", text_color="gray").pack(side="right")

        # Scrollable events box
        self.events_scrollbox = ctk.CTkScrollableFrame(list_frame, height=180, fg_color="#1a1a1a")
        self.events_scrollbox.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 15))

        # ---------------- Humanizer Randomness Settings ----------------
        settings_frame = ctk.CTkFrame(self, corner_radius=12)
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        settings_title = ctk.CTkLabel(
            settings_frame, 
            text="Human-like Randomness Controls", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        settings_title.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")

        # Info/Help button
        self.info_btn = ctk.CTkButton(
            settings_frame,
            text="ℹ",
            width=24,
            height=24,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#34495e",
            text_color="#3498db",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_sliders_help
        )
        self.info_btn.grid(row=0, column=1, padx=0, pady=(10, 5), sticky="w")

        self.reset_defaults_btn = ctk.CTkButton(
            settings_frame, 
            text="Reset Defaults", 
            width=100, 
            height=22, 
            fg_color="#34495e", 
            hover_color="#2c3e50", 
            text_color="white",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.reset_settings_defaults
        )
        self.reset_defaults_btn.grid(row=0, column=2, padx=15, pady=(10, 5), sticky="e")

        # 1. Timing variance slider
        ctk.CTkLabel(settings_frame, text="Timing Variance:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=15, pady=5, sticky="w")
        
        self.timing_slider = ctk.CTkSlider(
            settings_frame, 
            from_=0.0, 
            to=0.50, 
            number_of_steps=50,
            command=self._on_timing_slider_changed
        )
        self.timing_slider.set(self.humanizer.timing_variance)
        self.timing_slider.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.timing_lbl = ctk.CTkLabel(settings_frame, text="15%", width=50, anchor="e", font=ctk.CTkFont(weight="bold"))
        self.timing_lbl.grid(row=1, column=2, padx=15, pady=5, sticky="e")

        # 2. Position jitter slider
        ctk.CTkLabel(settings_frame, text="Position Jitter:", font=ctk.CTkFont(size=12)).grid(row=2, column=0, padx=15, pady=5, sticky="w")
        
        self.jitter_slider = ctk.CTkSlider(
            settings_frame, 
            from_=0, 
            to=15, 
            number_of_steps=15,
            command=self._on_jitter_slider_changed
        )
        self.jitter_slider.set(self.humanizer.position_jitter)
        self.jitter_slider.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.jitter_lbl = ctk.CTkLabel(settings_frame, text="3 px", width=50, anchor="e", font=ctk.CTkFont(weight="bold"))
        self.jitter_lbl.grid(row=2, column=2, padx=15, pady=5, sticky="e")

        # 3. Micro-pause chance slider
        ctk.CTkLabel(settings_frame, text="Micro-pause Chance:", font=ctk.CTkFont(size=12)).grid(row=3, column=0, padx=15, pady=5, sticky="w")
        
        self.pause_slider = ctk.CTkSlider(
            settings_frame, 
            from_=0.0, 
            to=0.10, 
            number_of_steps=20,
            command=self._on_pause_slider_changed
        )
        self.pause_slider.set(self.humanizer.pause_chance)
        self.pause_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.pause_lbl = ctk.CTkLabel(settings_frame, text="2%", width=50, anchor="e", font=ctk.CTkFont(weight="bold"))
        self.pause_lbl.grid(row=3, column=2, padx=15, pady=5, sticky="e")

        # 4. Loop delay slider & unit toggle
        ctk.CTkLabel(settings_frame, text="Loop Delay:", font=ctk.CTkFont(size=12)).grid(row=4, column=0, padx=15, pady=5, sticky="w")
        
        # Sub-container to hold slider and segmented button side-by-side
        delay_container = ctk.CTkFrame(settings_frame, fg_color="transparent")
        delay_container.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        self.loop_delay_slider = ctk.CTkSlider(
            delay_container, 
            from_=2.0, 
            to=60.0, 
            number_of_steps=58,
            command=self._on_loop_delay_slider_changed
        )
        self.loop_delay_slider.set(self.player.loop_delay)
        self.loop_delay_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.loop_delay_unit = ctk.CTkSegmentedButton(
            delay_container,
            values=["Sec", "Min"],
            width=70,
            command=self._on_loop_unit_changed
        )
        self.loop_delay_unit.set("Sec")
        self.loop_delay_unit.pack(side="right")
        
        self.loop_delay_lbl = ctk.CTkLabel(settings_frame, text="2s", width=50, anchor="e", font=ctk.CTkFont(weight="bold"))
        self.loop_delay_lbl.grid(row=4, column=2, padx=15, pady=5, sticky="e")

        settings_frame.grid_columnconfigure(1, weight=1)

        # ---------------- Status Panel ----------------
        status_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1e272e")
        status_frame.pack(fill="x", padx=20, pady=10)
        status_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.state_lbl = ctk.CTkLabel(status_frame, text="State: Idle", font=ctk.CTkFont(size=13, weight="bold"))
        self.state_lbl.grid(row=0, column=0, pady=8)

        self.loops_lbl = ctk.CTkLabel(status_frame, text="Loops Done: 0", font=ctk.CTkFont(size=13, weight="bold"))
        self.loops_lbl.grid(row=0, column=1, pady=8)

        self.events_lbl = ctk.CTkLabel(status_frame, text="Total Clicks: 0", font=ctk.CTkFont(size=13, weight="bold"))
        self.events_lbl.grid(row=0, column=2, pady=8)

        # ---------------- File Persistence Panel ----------------
        file_frame = ctk.CTkFrame(self, fg_color="transparent")
        file_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        self.save_btn = ctk.CTkButton(
            file_frame, 
            text="💾 Save Click Sequence", 
            fg_color="#8e44ad",
            hover_color="#732d91",
            command=self.save_sequence
        )
        self.save_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.load_btn = ctk.CTkButton(
            file_frame, 
            text="📂 Load Click Sequence", 
            fg_color="#2c3e50",
            hover_color="#1a252f",
            command=self.load_sequence
        )
        self.load_btn.pack(side="right", fill="x", expand=True, padx=(10, 0))

    # --- Slider Event Handlers ---
    def _on_timing_slider_changed(self, value):
        self.humanizer.timing_variance = float(value)
        self.timing_lbl.configure(text=f"{int(value * 100)}%")

    def _on_jitter_slider_changed(self, value):
        self.humanizer.position_jitter = int(value)
        self.jitter_lbl.configure(text=f"{int(value)} px")

    def _on_pause_slider_changed(self, value):
        self.humanizer.pause_chance = float(value)
        self.pause_lbl.configure(text=f"{int(value * 100)}%")

    def _on_loop_delay_slider_changed(self, value):
        unit = self.loop_delay_unit.get()
        if unit == "Sec":
            self.player.loop_delay = float(value)
            self.loop_delay_lbl.configure(text=f"{int(value)}s")
        else: # "Min"
            self.player.loop_delay = float(value) * 60.0
            self.loop_delay_lbl.configure(text=f"{float(value):.1f}m")

    def _on_loop_unit_changed(self, unit):
        if unit == "Sec":
            self.loop_delay_slider.configure(from_=2.0, to=60.0, number_of_steps=58)
            # Set to default: 2.0s
            val = 2.0
            self.loop_delay_slider.set(val)
            self.player.loop_delay = val
            self.loop_delay_lbl.configure(text="2s")
        else: # "Min"
            self.loop_delay_slider.configure(from_=1.0, to=10.0, number_of_steps=18) # 0.5m steps
            # Set to default: 1.0m (60.0s)
            val = 1.0
            self.loop_delay_slider.set(val)
            self.player.loop_delay = val * 60.0
            self.loop_delay_lbl.configure(text="1.0m")

    def reset_settings_defaults(self):
        # 1. Reset values in logic engines
        self.humanizer.timing_variance = 0.15
        self.humanizer.position_jitter = 3
        self.humanizer.pause_chance = 0.02
        self.player.loop_delay = 2.0

        # 2. Reset slider values
        self.timing_slider.set(0.15)
        self.jitter_slider.set(3)
        self.pause_slider.set(0.02)
        self.loop_delay_slider.configure(from_=2.0, to=60.0, number_of_steps=58)
        self.loop_delay_slider.set(2.0)
        self.loop_delay_unit.set("Sec")

        # 3. Update slider labels
        self.timing_lbl.configure(text="15%")
        self.jitter_lbl.configure(text="3 px")
        self.pause_lbl.configure(text="2%")
        self.loop_delay_lbl.configure(text="2s")

    def show_sliders_help(self):
        # Create a new top-level window
        help_win = ctk.CTkToplevel(self)
        help_win.title("ℹ Randomness Controls Guide")
        help_win.geometry("460x360")
        help_win.resizable(False, False)
        help_win.attributes('-topmost', True) # Keep on top of the main window

        # Main header
        header = ctk.CTkLabel(
            help_win, 
            text="Randomness Controls Guide", 
            font=ctk.CTkFont(family="Inter", size=18, weight="bold"),
            text_color="#3498db"
        )
        header.pack(pady=(15, 10))

        # Text area container
        text_frame = ctk.CTkFrame(help_win, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, padx=25, pady=10)

        help_text = (
            "🎯 Timing Variance\n"
            "Adds a random percentage variation to the delay intervals between actions "
            "(e.g., ±15%). This prevents perfect, robotic intervals.\n\n"
            "📍 Position Jitter\n"
            "Slightly offsets the clicked coordinates by a small random pixel amount "
            "(e.g., ±3px) to prevent clicking the exact same pixel repeatedly.\n\n"
            "☕ Micro-pause Chance\n"
            "The percentage chance of introducing a random, organic pause (50ms - 250ms) "
            "during replaying to simulate natural human hesitations.\n\n"
            "🔄 Loop Delay\n"
            "The customized delay pause between loop repetitions. Works in either "
            "seconds or minutes scale (supporting 2s up to 10m)."
        )

        content = ctk.CTkLabel(
            text_frame, 
            text=help_text, 
            justify="left", 
            wraplength=410,
            font=ctk.CTkFont(size=12)
        )
        content.pack(anchor="w")

        # Close button
        close_btn = ctk.CTkButton(
            help_win, 
            text="Close Guide", 
            fg_color="#34495e", 
            hover_color="#2c3e50",
            command=help_win.destroy
        )
        close_btn.pack(pady=(10, 15))

    # --- UI Status / Update Manager ---
    def _update_ui_state(self):
        # Update always-on-top attributes
        self.attributes('-topmost', self.always_on_top_switch.get())

        # Update button text/color based on running state
        if self.recorder.is_recording:
            self.record_btn.configure(text="⏹ Stop Rec (F6)", fg_color="#e74c3c", hover_color="#c0392b", text_color="white")
            self.play_btn.configure(state="disabled")
            self.clear_btn.configure(state="disabled")
            self.save_btn.configure(state="disabled")
            self.load_btn.configure(state="disabled")
            self.state_lbl.configure(text="State: RECORDING", text_color="#2ecc71")
        elif self.player.is_playing:
            self.record_btn.configure(state="disabled")
            self.play_btn.configure(text="⏹ Stop Play (F7)", fg_color="#e74c3c", hover_color="#c0392b", text_color="white")
            self.clear_btn.configure(state="disabled")
            self.save_btn.configure(state="disabled")
            self.load_btn.configure(state="disabled")
            self.state_lbl.configure(text="State: REPLAYING", text_color="#3498db")
        else:
            # Idle state
            self.record_btn.configure(state="normal", text="● Record (F6)", fg_color="#2ecc71", hover_color="#27ae60", text_color="black")
            self.play_btn.configure(state="normal" if self.sequence.events else "disabled", text="▶ Play Loop (F7)", fg_color="#3498db", hover_color="#2980b9", text_color="white")
            self.clear_btn.configure(state="normal" if self.sequence.events else "disabled")
            self.save_btn.configure(state="normal" if self.sequence.events else "disabled")
            self.load_btn.configure(state="normal")
            self.state_lbl.configure(text="State: Idle", text_color="white")
            self.loops_lbl.configure(text="Loops Done: 0")

        self.events_lbl.configure(text=f"Total Clicks: {len(self.sequence.events)}")

    def _toggle_always_on_top(self):
        self.attributes('-topmost', self.always_on_top_switch.get())

    # --- Thread-Safe Callbacks ---
    def _safe_on_record_event(self, event: ClickEvent):
        # Tkinter requires scheduling updates on the main event thread
        self.after(0, self._on_record_event, event)

    def _on_record_event(self, event: ClickEvent):
        self.sequence.add_event(event)
        self._add_event_to_feed_ui(event, len(self.sequence.events))
        self._update_ui_state()

    def _safe_on_loop_complete(self, loops: int):
        self.after(0, self._on_loop_complete, loops)

    def _on_loop_complete(self, loops: int):
        self.loops_lbl.configure(text=f"Loops Done: {loops}")

    def _safe_on_playback_stopped(self):
        self.after(0, self._on_playback_stopped)

    def _on_playback_stopped(self):
        self._update_ui_state()

    # --- UI Table Manipulation ---
    def _add_event_to_feed_ui(self, event: ClickEvent, index: int):
        # Create row frame
        row = ctk.CTkFrame(self.events_scrollbox, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        # Format values
        action_name = f"{event.button.capitalize()} {event.action.capitalize()}"
        pos_str = f"({event.x}, {event.y})"
        delay_str = f"{event.delay:.3f}s"

        ctk.CTkLabel(row, text=str(index), width=50, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=action_name, width=120, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=pos_str, width=150, anchor="w").pack(side="left")
        ctk.CTkLabel(row, text=delay_str, width=100, anchor="e").pack(side="right")

    def _rebuild_events_feed_ui(self):
        # Clear current feed UI widgets
        for widget in self.events_scrollbox.winfo_children():
            widget.destroy()

        # Add all currently loaded events
        for idx, event in enumerate(self.sequence.events, 1):
            self._add_event_to_feed_ui(event, idx)

    # --- Main Actions ---
    def toggle_recording(self):
        if self.player.is_playing:
            return  # Can't record while replaying

        if self.recorder.is_recording:
            # Stop recording
            self.recorder.stop()
            self._update_ui_state()
        else:
            # Start recording
            # Reset current list if they record a new sequence
            if self.sequence.events:
                if messagebox.askyesno("New Recording", "Recording a new sequence will overwrite the existing one. Do you want to continue?"):
                    self.clear_sequence()
                else:
                    return
            
            self.recorder.start()
            self._update_ui_state()

    def toggle_playback(self):
        if self.recorder.is_recording:
            return  # Can't play while recording

        if self.player.is_playing:
            # Stop playback
            self.player.stop()
            self._update_ui_state()
        else:
            # Start playback
            if not self.sequence.events:
                return
            
            # Start playing events
            self.player.start(self.sequence.events)
            self._update_ui_state()

    def stop_all(self):
        # Global halt button
        if self.recorder.is_recording:
            self.recorder.stop()
        if self.player.is_playing:
            self.player.stop()
        self._update_ui_state()

    def clear_sequence(self):
        self.recorder.clear()
        self.sequence.clear()
        self._rebuild_events_feed_ui()
        self._update_ui_state()

    # --- Persistence Handlers ---
    def save_sequence(self):
        if not self.sequence.events:
            messagebox.showwarning("Save Blocked", "No click events recorded to save.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Sequence"
        )
        if filepath:
            try:
                self.sequence.save_to_file(filepath)
                messagebox.showinfo("Success", f"Sequence successfully saved to:\n{os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save sequence:\n{e}")

    def load_sequence(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")],
            title="Load Sequence"
        )
        if filepath:
            try:
                new_seq = Sequence.load_from_file(filepath)
                self.sequence = new_seq
                self._rebuild_events_feed_ui()
                self._update_ui_state()
                messagebox.showinfo("Success", f"Sequence loaded with {len(self.sequence.events)} clicks.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load sequence:\n{e}")

    # --- Cleanup On Close ---
    def _on_closing(self):
        self.hotkeys.stop()
        self.recorder.stop()
        self.player.stop()
        self.destroy()
