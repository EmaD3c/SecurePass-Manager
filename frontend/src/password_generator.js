document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const copyBtn = document.getElementById('copy-btn');
    const passwordInput = document.getElementById('password');
    const lengthInput = document.getElementById('length');
    const upperCheckbox = document.getElementById('upper');
    const lowerCheckbox = document.getElementById('lower');
    const digitsCheckbox = document.getElementById('digits');
    const specialCheckbox = document.getElementById('special');
    const strengthBar = document.querySelector('.strength-bar');
    const strengthText = document.querySelector('.strength-text');

    generateBtn.addEventListener('click', generatePassword);
    copyBtn.addEventListener('click', copyPassword);

    async function generatePassword() {
        const length = parseInt(lengthInput.value);
        const upper = upperCheckbox.checked;
        const lower = lowerCheckbox.checked;
        const digits = digitsCheckbox.checked;
        const special = specialCheckbox.checked;

        try {
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';

            const response = await fetch("http://localhost:8000/api/auth/generate-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    length: length,
                    upper: upper,
                    lower: lower,
                    digits: digits,
                    special: special,
                }),
            });

            const data = await response.json();

            passwordInput.value = data.password;
            updatePasswordStrength(data.password);
        } catch (error) {
            console.error("Error:", error);
            alert(error.message);
        } finally {
            generateBtn.disabled = false;
            generateBtn.textContent = 'Generate';
        }
    }

    function copyPassword() {
        if (!passwordInput.value) return;
        
        passwordInput.select();
        document.execCommand('copy');
        
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copy!';
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);
    }

    function updatePasswordStrength(password) {
        if (!password) return;
        
        let strength = 0;
        if (password.length >= 12) strength += 1;
        if (password.length >= 16) strength += 1;

        if (/[A-Z]/.test(password)) strength += 1;
        if (/[a-z]/.test(password)) strength += 1;
        if (/[0-9]/.test(password)) strength += 1;
        if (/[^A-Za-z0-9]/.test(password)) strength += 1;
        
        // // Percentage calculation
        const strengthPercent = Math.min(100, (strength / 6) * 100);
        
        // Visual update
        strengthBar.style.width = `${strengthPercent}%`;
        
        if (strengthPercent < 40) {
            strengthBar.style.backgroundColor = '#ff4d4d';
            strengthText.textContent = 'Password strength: Weak';
        } else if (strengthPercent < 70) {
            strengthBar.style.backgroundColor = '#ffcc00';
            strengthText.textContent = 'Password strength: Medium';
        } else {
            strengthBar.style.backgroundColor = '#4CAF50';
            strengthText.textContent = 'Password strength: Strong';
        }
    }
});