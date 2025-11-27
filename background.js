/**
 * Background Service Worker for Gmail Phishing Detector
 * 
 * This script runs in the background and handles extension lifecycle events.
 * Currently, it serves as a placeholder for future background logic, such as
 * handling browser actions, context menus, or cross-origin requests that 
 * cannot be handled by content scripts directly.
 */

// Listener for when the extension is installed or updated.
chrome.runtime.onInstalled.addListener(() => {
    console.log("Gmail Phishing Detector extension installed.");
});
