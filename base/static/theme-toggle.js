/**
 * Theme Toggle System for Habit Tracker
 * Handles Light/Dark mode switching with localStorage persistence
 */

(function() {
    'use strict';

    const THEME_KEY = 'habit-tracker-theme';
    const THEME_CLASS = 'dark-theme';
    
    /**
     * Get current theme from localStorage or system preference
     */
    function getCurrentTheme() {
        // Check localStorage first
        const savedTheme = localStorage.getItem(THEME_KEY);
        if (savedTheme) {
            return savedTheme;
        }
        
        // Fallback to system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        
        return 'light';
    }
    
    /**
     * Apply theme to the document
     */
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add(THEME_CLASS);
        } else {
            document.body.classList.remove(THEME_CLASS);
        }
        
        // Update toggle button icon if it exists
        updateToggleIcon(theme);
    }
    
    /**
     * Update toggle button icon
     */
    function updateToggleIcon(theme) {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            const icon = toggleBtn.querySelector('.theme-icon');
            if (icon) {
                icon.textContent = theme === 'dark' ? '☀️' : '🌙';
            }
            toggleBtn.setAttribute('aria-label', 
                theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
            );
            toggleBtn.setAttribute('title', 
                theme === 'dark' ? 'Light Mode' : 'Dark Mode'
            );
        }
    }
    
    /**
     * Toggle between light and dark theme
     */
    function toggleTheme() {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Save to localStorage
        localStorage.setItem(THEME_KEY, newTheme);
        
        // Apply theme
        applyTheme(newTheme);
    }
    
    /**
     * Initialize theme system
     */
    function initTheme() {
        // Apply saved or default theme immediately (before page renders)
        const theme = getCurrentTheme();
        applyTheme(theme);
        
        // Set up toggle button listener when DOM is ready
        document.addEventListener('DOMContentLoaded', function() {
            const toggleBtn = document.getElementById('theme-toggle');
            if (toggleBtn) {
                toggleBtn.addEventListener('click', toggleTheme);
                updateToggleIcon(theme);
            }
        });
        
        // Listen for system theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                // Only apply if user hasn't manually set a theme
                if (!localStorage.getItem(THEME_KEY)) {
                    applyTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
    }
    
    // Initialize immediately to prevent flash
    initTheme();
    
    // Expose toggle function globally for inline event handlers if needed
    window.toggleTheme = toggleTheme;
})();
