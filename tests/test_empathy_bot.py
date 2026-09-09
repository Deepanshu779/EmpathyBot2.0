import unittest
import os
import pandas as pd
from utils.bot_engine import (
    check_crisis,
    detect_mood,
    get_offline_response,
    get_configured_api_key
)
from utils.data_store import (
    init_data_store,
    load_mood_logs,
    append_mood_log,
    populate_sample_data,
    delete_mood_log,
    get_log_filepath
)

class TestEmpathyBotEngine(unittest.TestCase):

    def test_crisis_detection(self):
        """Ensures critical self-harm keywords trigger crisis safeguard."""
        crisis_samples = [
            "I want to kill myself",
            "thinking about ending it all",
            "I don't want to live anymore",
            "self-harm impulses are strong"
        ]
        for text in crisis_samples:
            self.assertTrue(check_crisis(text), f"Failed to detect crisis in: {text}")

    def test_crisis_no_false_positives(self):
        """Verifies innocent sentences do not trigger crisis safeguards."""
        safe_samples = [
            "I am starting a healthy diet tomorrow",
            "We rolled the die and won the game",
            "I died laughing at that comedy show"
        ]
        # 'diet' should not trigger 'die'
        self.assertFalse(check_crisis(safe_samples[0]))

    def test_mood_detection(self):
        """Checks accurate classification of core emotional tones."""
        self.assertEqual(detect_mood("I am so happy and excited today!"), "happy")
        self.assertEqual(detect_mood("I feel really anxious and stressed about exams"), "anxious")
        self.assertEqual(detect_mood("I feel completely drained, exhausted and tired"), "tired")
        self.assertEqual(detect_mood("My ex broke my heart, we had a painful breakup"), "breakup")
        self.assertEqual(detect_mood("I can't sleep at night, insomnia is getting worse"), "insomnia")
        self.assertEqual(detect_mood("Thank you so much for your help"), "gratitude")

    def test_offline_personas(self):
        """Ensures each persona produces tailored, non-empty empathetic responses."""
        personas = ["🌿 Serene", "⚡ Joy", "🧠 Sage"]
        moods = ["happy", "sad", "anxious", "tired", "neutral"]
        
        for p in personas:
            for m in moods:
                reply = get_offline_response(p, m)
                self.assertTrue(len(reply) > 20, f"Response too short for {p} on {m}")
                self.assertIsInstance(reply, str)

    def test_configured_api_key_type(self):
        """Verifies API key getter safely returns a string."""
        key = get_configured_api_key()
        self.assertIsInstance(key, str)


class TestDataStore(unittest.TestCase):

    def setUp(self):
        # Ensure log file initialized
        init_data_store()

    def test_append_and_load(self):
        """Tests adding an entry and verifying it appears in the DataFrame."""
        initial_df = load_mood_logs()
        initial_count = len(initial_df)
        
        success = append_mood_log(
            score=7.5,
            mood="happy",
            influencers=["Sleep", "Exercise"],
            notes="Unit test log entry"
        )
        self.assertTrue(success)
        
        updated_df = load_mood_logs()
        self.assertEqual(len(updated_df), initial_count + 1)
        last_row = updated_df.iloc[-1]
        self.assertEqual(last_row["mood"], "happy")
        self.assertAlmostEqual(last_row["score"], 7.5)
        self.assertIn("Sleep", last_row["influencers"])

    def test_sample_data_population(self):
        """Tests populating 14 days of mock data."""
        populate_sample_data()
        df = load_mood_logs()
        self.assertGreaterEqual(len(df), 14)
        self.assertIn("score", df.columns)
        self.assertIn("mood", df.columns)
        self.assertIn("influencers", df.columns)

    def test_delete_mood_log(self):
        """Tests removing an entry by index."""
        populate_sample_data()
        df_before = load_mood_logs()
        count_before = len(df_before)
        
        deleted = delete_mood_log(0)
        self.assertTrue(deleted)
        
        df_after = load_mood_logs()
        self.assertEqual(len(df_after), count_before - 1)


if __name__ == '__main__':
    unittest.main()
