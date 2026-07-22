import express from 'express';
import { validationResult } from 'express-validator';
import db from '../db';

const router = express.Router();

// Middleware to parse JSON request bodies
router.use(express.json());

// Route handler for subscribing a user to notification types
router.post('/subscribe', (req, res) => {
    // Validate incoming request data
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
    }

    // Extract userId and notificationTypes from the request body
    const { userId, notificationTypes } = req.body;

    // Validate required fields and data types
    if (!userId || !notificationTypes || !Array.isArray(notificationTypes)) {
        return res.status(400).json({ error: 'Invalid input' });
    }

    // Insert user notifications into the database
    db.query('INSERT INTO user_notifications (user_id, notification_types) VALUES (?, ?)', [userId, JSON.stringify(notificationTypes)], (err, result) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to subscribe' });
        }
        res.status(201).json({ message: 'Subscribed successfully' });
    });
});

export default router;
