import cv2
import numpy as np

class UIRenderer:
    def __init__(self):
        # Use a thicker, modern looking font
        self.font = cv2.FONT_HERSHEY_DUPLEX
        
    def _draw_text_with_bg(self, img, text, pos, font_scale, font_thickness, text_color, bg_color, padding=15, radius=10):
        x, y = pos
        (text_w, text_h), _ = cv2.getTextSize(text, self.font, font_scale, font_thickness)
        
        rx1, ry1 = x - padding, y - text_h - padding
        rx2, ry2 = x + text_w + padding, y + padding

        # Rounded-rect background (approximated with rectangle + circles at corners)
        cv2.rectangle(img, (rx1 + radius, ry1), (rx2 - radius, ry2), bg_color, -1)
        cv2.rectangle(img, (rx1, ry1 + radius), (rx2, ry2 - radius), bg_color, -1)
        for cx, cy in [(rx1+radius, ry1+radius), (rx2-radius, ry1+radius),
                       (rx1+radius, ry2-radius), (rx2-radius, ry2-radius)]:
            cv2.circle(img, (cx, cy), radius, bg_color, -1)

        # White border
        cv2.rectangle(img, (rx1, ry1), (rx2, ry2), (255, 255, 255), max(1, font_thickness - 1))
        
        # Text shadow for depth
        cv2.putText(img, text, (x + 2, y + 2), self.font, font_scale, (0, 0, 0), font_thickness)
        # Actual text
        cv2.putText(img, text, (x, y), self.font, font_scale, text_color, font_thickness)
        return text_w, text_h

    def draw(self, frame, question, score, streak, engagement, hover_zone, hover_progress):
        h, w, _ = frame.shape
        
        # Draw Quadrants (A, B, C, D) with thicker lines
        cv2.line(frame, (w//2, 0), (w//2, h), (255, 255, 255), 3)
        cv2.line(frame, (0, h//2), (w, h//2), (255, 255, 255), 3)
        
        # Vibrant colors for kids (BGR format)
        zones = {
            "A": {"pos": (w//4, h//4), "rect": (0, 0, w//2, h//2), "color": (130, 220, 255)},   # Yellowish
            "B": {"pos": (3*w//4, h//4), "rect": (w//2, 0, w, h//2), "color": (150, 250, 150)},  # Greenish
            "C": {"pos": (w//4, 3*h//4), "rect": (0, h//2, w//2, h), "color": (255, 150, 150)},  # Blueish
            "D": {"pos": (3*w//4, 3*h//4), "rect": (w//2, h//2, w, h), "color": (200, 150, 255)},  # Pinkish
        }

        # Highlight hovered zone
        if hover_zone in zones:
            overlay = frame.copy()
            x1, y1, x2, y2 = zones[hover_zone]["rect"]
            cv2.rectangle(overlay, (x1, y1), (x2, y2), zones[hover_zone]["color"], -1)
            # Alpha blend
            alpha = 0.4 * hover_progress
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
            
            # Progress bar at the bottom of the quadrant
            bar_w = int((x2 - x1) * hover_progress)
            cv2.rectangle(frame, (x1, y2 - 15), (x1 + bar_w, y2), (0, 255, 255), -1) # Yellow progress bar

        # ── Question Banner (top-center, clear of the score) ──────────────────
        if question:
            q_text = question["q"]
            (q_tw, q_th), _ = cv2.getTextSize(q_text, self.font, 1.2, 3)
            # Center horizontally, sit at top with comfortable margin
            q_x = (w - q_tw) // 2
            q_y = 55
            self._draw_text_with_bg(frame, q_text, (q_x, q_y), 1.2, 3, (255, 255, 255), (100, 40, 40))

            # Draw Options in Zones
            for z_key, z_data in zones.items():
                opt_text = f"{z_key}: {question['opts'][z_key]}"
                x, y = z_data["pos"]
                (tw, th), _ = cv2.getTextSize(opt_text, self.font, 1.2, 3)
                bg_c = tuple(int(c * 0.6) for c in z_data["color"])
                self._draw_text_with_bg(frame, opt_text, (x - tw//2, y), 1.2, 3, (255, 255, 255), bg_c)

        else:
            msg = "GAME OVER! Press R to Restart"
            (gw, gh), _ = cv2.getTextSize(msg, self.font, 1.5, 3)
            self._draw_text_with_bg(frame, msg, ((w - gw) // 2, h // 2), 1.5, 3, (255, 255, 255), (0, 0, 200))

        # ── Score Pill — bottom-left corner ─────────────────────────────────────
        score_text  = f"  SCORE: {score}  "
        streak_text = f"  STREAK: {streak}x  "

        (sw, sh), _ = cv2.getTextSize(score_text,  self.font, 1.0, 2)
        (kw, kh), _ = cv2.getTextSize(streak_text, self.font, 1.0, 2)

        margin  = 18   # distance from edge
        padding = 12   # inner padding
        gap     = 10   # gap between the two pills

        # Score pill – bottom-left
        s_x = margin
        s_y = h - margin
        self._draw_text_with_bg(frame, score_text,  (s_x, s_y), 1.0, 2, (0, 255, 200), (30, 90, 30), padding=padding)

        # Streak pill – just to the right of the score pill
        k_x = s_x + sw + gap + padding * 2
        k_y = s_y
        self._draw_text_with_bg(frame, streak_text, (k_x, k_y), 1.0, 2, (255, 220, 0), (90, 60, 0), padding=padding)

        # Removed the engagement state text as requested

        return frame
