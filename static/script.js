function copyCode() {
    const codeElement = document.getElementById('yaml-content');
    const text = codeElement.textContent;
    
    navigator.clipboard.writeText(text).then(() => {
        const button = document.querySelector('.copy-button');
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg> Copy`;
        }, 2000);
    });
}

// Spinning
const spinner = document.querySelector('.spin-container')
const submitBtn = document.getElementById('generateBtn')

submitBtn.addEventListener('click', () => {
    console.log('click');
    
    spinner.classList.add('spinning');
})

// Apply syntax highlighting to YAML content
document.addEventListener('DOMContentLoaded', (event) => {
    Prism.highlightAll();
});