// Modern JavaScript for Resume AI Generator

class ResumeGenerator {
    constructor() {
        this.jobDescription = '';
        this.goodResume = '';
        this.badResume = '';
        this.nonNegotiables = [];
        this.niceToHaves = [];
        this.initializeEventListeners();
        this.initializeScrollEffects();
    }

    initializeEventListeners() {
        // Main generate button
        const generateBtn = document.getElementById('generateBtn');
        generateBtn.addEventListener('click', () => this.generateResumes());

        // File upload
        const fileInput = document.getElementById('fileInput');
        fileInput.addEventListener('change', (e) => this.handleFileUpload(e));

        // Export PDF button
        const exportPdfBtn = document.getElementById('exportPdfBtn');
        if (exportPdfBtn) {
            exportPdfBtn.addEventListener('click', () => this.exportPDFs());
        }

        // New analysis button
        const newAnalysisBtn = document.getElementById('newAnalysisBtn');
        if (newAnalysisBtn) {
            newAnalysisBtn.addEventListener('click', () => this.resetToInput());
        }

        // Copy buttons
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.copyResume(e.target.closest('.copy-btn')));
        });

        // Download buttons
        document.querySelectorAll('.download-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.downloadResume(e.target.closest('.download-btn')));
        });

        // Modal functionality
        this.initializeModal();

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const generateBtn = document.getElementById('generateBtn');
                    if (generateBtn && !generateBtn.disabled) {
                        this.generateResumes();
                    }
                }
            }
        });

        // Auto-resize textarea
        const textarea = document.getElementById('jobDescription');
        textarea.addEventListener('input', this.autoResizeTextarea);
    }

    initializeScrollEffects() {
        // Smooth reveal animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.input-card, .resume-card, .insight-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    }

    autoResizeTextarea(e) {
        const textarea = e.target;
        textarea.style.height = 'auto';
        textarea.style.height = Math.max(textarea.scrollHeight, 400) + 'px';
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        if (!file.type.includes('text')) {
            this.showToast('Please select a text file (.txt, .md)', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            document.getElementById('jobDescription').value = content;
            this.showToast('File loaded successfully!', 'success');
            
            // Auto-resize after loading
            const textarea = document.getElementById('jobDescription');
            this.autoResizeTextarea({ target: textarea });
        };
        reader.onerror = () => {
            this.showToast('Error reading file', 'error');
        };
        reader.readAsText(file);
    }

    async generateResumes() {
        // Collect non-negotiables
        this.nonNegotiables = [];
        document.querySelectorAll('#nonNegotiables .requirement-input').forEach(input => {
            if (input.value.trim()) {
                this.nonNegotiables.push(input.value.trim());
            }
        });

        // Collect nice-to-haves
        this.niceToHaves = [];
        document.querySelectorAll('#niceToHaves .requirement-input').forEach(input => {
            if (input.value.trim()) {
                this.niceToHaves.push(input.value.trim());
            }
        });

        if (this.nonNegotiables.length === 0) {
            this.showToast('Please add at least one non-negotiable requirement', 'error');
            return;
        }

        // Format the job description
        let jobDescription = 'Job Requirements:\n\n';
        jobDescription += 'NON-NEGOTIABLES (Must Have):\n';
        this.nonNegotiables.forEach((req, index) => {
            jobDescription += `${index + 1}. ${req}\n`;
        });

        if (this.niceToHaves.length > 0) {
            jobDescription += '\nNICE TO HAVES (Preferred):\n';
            this.niceToHaves.forEach((req, index) => {
                jobDescription += `${index + 1}. ${req}\n`;
            });
        }

        this.jobDescription = jobDescription;

        // Show loading state
        this.showLoadingState();
        
        // Add some visual feedback
        this.startLoadingAnimation();

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ job_description: jobDescription })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Generation failed');
            }

            this.goodResume = data.good_resume;
            this.badResume = data.bad_resume;

            // Simulate minimum loading time for better UX
            setTimeout(() => {
                this.showResults();
                this.showToast('Resumes generated successfully!', 'success');
            }, 1500);

        } catch (error) {
            console.error('Generation error:', error);
            this.hideLoadingState();
            this.showToast(error.message || 'Failed to generate resumes. Please try again.', 'error');
        }
    }

    startLoadingAnimation() {
        const progressFill = document.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.style.animation = 'none';
            setTimeout(() => {
                progressFill.style.animation = 'progress 3s infinite';
            }, 100);
        }
    }

    showLoadingState() {
        const inputSection = document.querySelector('.input-section');
        const loadingSection = document.getElementById('loadingSection');
        const resultsSection = document.getElementById('resultsSection');
        
        if (inputSection) inputSection.style.display = 'none';
        if (resultsSection) resultsSection.style.display = 'none';
        if (loadingSection) {
            loadingSection.style.display = 'block';
            // Trigger reflow for animation
            loadingSection.offsetHeight;
        }

        // Update page title
        document.title = '🎯 Generating Examples... - Resume Screening Assistant';
    }

    hideLoadingState() {
        const inputSection = document.querySelector('.input-section');
        const loadingSection = document.getElementById('loadingSection');
        
        if (loadingSection) loadingSection.style.display = 'none';
        if (inputSection) inputSection.style.display = 'block';

        // Restore page title
        document.title = '🎯 Resume Screening Assistant';
    }

    showResults() {
        const loadingSection = document.getElementById('loadingSection');
        const resultsSection = document.getElementById('resultsSection');
        const badResumeContent = document.getElementById('badResumeContent');
        const goodResumeContent = document.getElementById('goodResumeContent');
        const heroSection = document.querySelector('.hero');
        const inputSection = document.querySelector('.input-section');

        if (loadingSection) loadingSection.style.display = 'none';
        if (heroSection) heroSection.style.display = 'none';
        if (inputSection) inputSection.style.display = 'none';
        
        if (resultsSection) {
            resultsSection.style.display = 'block';
            // Smooth scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        if (badResumeContent) badResumeContent.textContent = this.badResume;
        if (goodResumeContent) goodResumeContent.textContent = this.goodResume;

        // Populate criteria evaluation
        this.populateEvaluation();

        // Update page title
        document.title = '📋 Candidate Examples - Resume Screening Assistant';

        // Trigger animations
        setTimeout(() => {
            document.querySelectorAll('.resume-card').forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(30px)';
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 200);
            });
        }, 100);
    }

    async populateEvaluation() {
        const rejectCriteria = document.getElementById('rejectCriteria');
        const acceptCriteria = document.getElementById('acceptCriteria');

        if (!rejectCriteria || !acceptCriteria) return;

        // Show loading message
        rejectCriteria.innerHTML = '<div class="loading-analysis">🤖 AI is analyzing resume criteria...</div>';
        acceptCriteria.innerHTML = '<div class="loading-analysis">🤖 AI is analyzing resume criteria...</div>';

        try {
            // Analyze bad resume (reject criteria)
            this.currentlyEvaluatingGoodResume = false;
            rejectCriteria.innerHTML = '';
            
            for (const requirement of this.nonNegotiables) {
                const actuallyMeetsRequirement = await this.doesResumeMeetRequirement(this.badResume, requirement);
                const criteriaItem = this.createCriteriaItem(requirement, actuallyMeetsRequirement, true);
                rejectCriteria.appendChild(criteriaItem);
            }

            for (const requirement of this.niceToHaves) {
                const actuallyMeetsRequirement = await this.doesResumeMeetRequirement(this.badResume, requirement);
                const criteriaItem = this.createCriteriaItem(requirement, actuallyMeetsRequirement, false);
                rejectCriteria.appendChild(criteriaItem);
            }

            // Analyze good resume (accept criteria)
            this.currentlyEvaluatingGoodResume = true;
            acceptCriteria.innerHTML = '';
            
            for (const requirement of this.nonNegotiables) {
                const actuallyMeetsRequirement = await this.doesResumeMeetRequirement(this.goodResume, requirement);
                const criteriaItem = this.createCriteriaItem(requirement, actuallyMeetsRequirement, true);
                acceptCriteria.appendChild(criteriaItem);
            }

            for (const requirement of this.niceToHaves) {
                const actuallyMeetsRequirement = await this.doesResumeMeetRequirement(this.goodResume, requirement);
                const criteriaItem = this.createCriteriaItem(requirement, actuallyMeetsRequirement, false);
                acceptCriteria.appendChild(criteriaItem);
            }
            
        } catch (error) {
            console.error('Error during evaluation:', error);
            rejectCriteria.innerHTML = '<div class="error-analysis">❌ Error analyzing criteria</div>';
            acceptCriteria.innerHTML = '<div class="error-analysis">❌ Error analyzing criteria</div>';
        }
    }

    async doesResumeMeetRequirement(resumeText, requirement) {
        if (!resumeText || !requirement) return false;
        
        try {
            const response = await fetch('/analyze-requirement', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    requirement: requirement,
                    resume_text: resumeText
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Store the AI analysis for later use
                this.lastAnalysis = result;
                return result.meets_requirement;
            } else {
                console.error('Analysis failed:', result.error);
                return false;
            }
        } catch (error) {
            console.error('Error analyzing requirement:', error);
            return false;
        }
    }

    createCriteriaItem(requirement, passed, isNonNegotiable) {
        const item = document.createElement('div');
        item.className = 'criteria-item';

        const icon = document.createElement('span');
        icon.className = `criteria-icon ${passed ? 'pass' : 'fail'}`;
        icon.textContent = passed ? '✅' : '❌';

        const textDiv = document.createElement('div');
        textDiv.className = 'criteria-text';

        const requirementDiv = document.createElement('div');
        requirementDiv.className = 'criteria-requirement';
        requirementDiv.textContent = requirement;

        const statusDiv = document.createElement('div');
        statusDiv.className = 'criteria-status';
        
        // Generate realistic explanations based on the requirement
        const explanation = this.generateCriteriaExplanation(requirement, passed, isNonNegotiable);
        statusDiv.textContent = explanation;
        
        if (passed) {
            statusDiv.style.color = 'var(--secondary-color)';
        } else {
            statusDiv.style.color = isNonNegotiable ? 'var(--danger-color)' : 'var(--text-muted)';
        }

        textDiv.appendChild(requirementDiv);
        textDiv.appendChild(statusDiv);

        // Add Show Examples button
        const examplesBtn = document.createElement('button');
        examplesBtn.className = 'examples-btn';
        examplesBtn.innerHTML = '<i class="fas fa-search"></i> Show Examples';
        examplesBtn.addEventListener('click', () => {
            console.log('Show Examples clicked for:', requirement);
            // Determine if this is from accept or reject section
            const isFromAcceptSection = item.closest('#acceptCriteria') !== null;
            this.showExamples(requirement, passed, isNonNegotiable, isFromAcceptSection);
        });

        item.appendChild(icon);
        item.appendChild(textDiv);
        item.appendChild(examplesBtn);

        return item;
    }

    generateCriteriaExplanation(requirement, passed, isNonNegotiable) {
        // Use the AI analysis that was stored when checking the requirement
        if (this.lastAnalysis && this.lastAnalysis.explanation) {
            return this.lastAnalysis.explanation;
        }
        
        return passed ? 'Requirement appears to be met.' : 'No clear evidence found.';
    }

    showExamples(requirement, passed, isNonNegotiable, isFromAcceptSection) {
        console.log('showExamples called:', { requirement, passed, isNonNegotiable, isFromAcceptSection });
        
        const modal = document.getElementById('examplesModal');
        const modalBody = document.getElementById('examplesModalBody');
        
        console.log('Modal elements:', { modal: !!modal, modalBody: !!modalBody });
        
        if (!modal || !modalBody) {
            console.error('Modal elements not found!');
            return;
        }

        // Use the section parameter to determine which resume to show
        const currentResume = isFromAcceptSection ? this.goodResume : this.badResume;
        const resumeType = isFromAcceptSection ? 'ACCEPT' : 'REJECT';
        
        // Get fresh AI analysis for this specific requirement and resume
        this.getAIAnalysisForModal(requirement, currentResume, resumeType, modal, modalBody, passed, isNonNegotiable);
    }

    async getAIAnalysisForModal(requirement, resumeText, resumeType, modal, modalBody, passed, isNonNegotiable) {
        // Show loading in modal
        modalBody.innerHTML = `
            <h3><i class="fas fa-search"></i> Resume Evidence</h3>
            <div class="requirement-header">
                <h4>${passed ? '✅' : '❌'} ${requirement}</h4>
                <p class="requirement-type">${isNonNegotiable ? 'Non-Negotiable Requirement' : 'Nice to Have'}</p>
            </div>
            
            <div class="examples-content">
                <div class="loading-analysis">🤖 AI is analyzing the resume...</div>
            </div>
        `;
        
        modal.style.display = 'block';
        
        try {
            const response = await fetch('/analyze-requirement', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    requirement: requirement,
                    resume_text: resumeText
                })
            });
            
            const result = await response.json();
            
            if (response.ok) {
                modalBody.innerHTML = `
                    <h3><i class="fas fa-search"></i> Resume Evidence</h3>
                    <div class="requirement-header">
                        <h4>${result.meets_requirement ? '✅' : '❌'} ${requirement}</h4>
                        <p class="requirement-type">${isNonNegotiable ? 'Non-Negotiable Requirement' : 'Nice to Have'}</p>
                    </div>
                    
                    <div class="examples-content">
                        <div class="resume-example">
                            <h5>${resumeType} Resume - AI Analysis:</h5>
                            <div class="example-text">
                                <p><strong>Analysis:</strong> ${result.explanation}</p>
                                <p><strong>Supporting Evidence:</strong></p>
                                <pre class="resume-excerpt">${result.evidence}</pre>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                modalBody.innerHTML += `<div class="error-analysis">❌ Error: ${result.error}</div>`;
            }
        } catch (error) {
            console.error('Error getting AI analysis:', error);
            modalBody.innerHTML += `<div class="error-analysis">❌ Failed to get AI analysis</div>`;
        }
    }

    findEvidenceInResume(resumeText, requirement) {
        if (!resumeText) {
            return {
                found: false,
                explanation: 'Resume content not available for analysis.',
                excerpt: 'No content to display.'
            };
        }

        const req = requirement.toLowerCase();
        const resumeLower = resumeText.toLowerCase();
        
        
        // Look for specific patterns based on requirement type
        if (req.includes('degree') || req.includes('bachelor') || req.includes('master')) {
            const educationSection = this.extractSection(resumeText, ['education', 'academic']);
            
            // Check for any degree first
            const hasDegree = resumeLower.includes('bachelor') || resumeLower.includes('master') || 
                            resumeLower.includes('b.s.') || resumeLower.includes('m.s.') ||
                            resumeLower.includes('degree');
            
            // Check if requirement specifies a field and if so, verify field match
            let fieldMatch = true;
            
            // Extract field from requirement
            if (req.includes('computer science') || req.includes('computer')) {
                fieldMatch = resumeLower.includes('computer science') || resumeLower.includes('computer');
            } else if (req.includes('engineering')) {
                fieldMatch = resumeLower.includes('engineering');
            } else if (req.includes('business')) {
                fieldMatch = resumeLower.includes('business');
            } else if (req.includes('marketing')) {
                fieldMatch = resumeLower.includes('marketing');
            } else if (req.includes('data science') || req.includes('statistics')) {
                fieldMatch = resumeLower.includes('data science') || resumeLower.includes('statistics') || resumeLower.includes('data');
            } else if (req.includes('finance')) {
                fieldMatch = resumeLower.includes('finance');
            } else if (req.includes('mathematics') || req.includes('math')) {
                fieldMatch = resumeLower.includes('mathematics') || resumeLower.includes('math');
            } else {
                // If requirement mentions a specific field that we don't handle above,
                // try to extract it and check for exact match
                const fieldWords = req.match(/(?:degree|bachelor|master|phd).*?in\s+([^,\n]+)/i);
                if (fieldWords && fieldWords[1]) {
                    const requiredField = fieldWords[1].trim().toLowerCase();
                    fieldMatch = resumeLower.includes(requiredField);
                }
            }
            
            const meetsRequirement = hasDegree && fieldMatch;
            
            
            return {
                found: meetsRequirement,
                explanation: meetsRequirement ? 
                    'The candidate has the required educational background.' :
                    hasDegree ? 'The candidate has a degree but not in the required field.' :
                    'No formal degree is listed in the education section.',
                excerpt: educationSection || this.getResumeSnippet(resumeText, 300)
            };
        }
        
        if (req.includes('year') && req.includes('experience')) {
            const experienceSection = this.extractSection(resumeText, ['experience', 'employment', 'work history']);
            
            // Extract required years from the requirement (e.g., "5+ years" -> 5)
            const requiredYearsMatch = req.match(/(\d+)\s*[\+\-]?\s*year/);
            const requiredYears = requiredYearsMatch ? parseInt(requiredYearsMatch[1]) : 1;
            
            // Look for years of experience mentioned in the resume
            const resumeYearsMatch = resumeText.match(/(\d+)\s*[\+\-]?\s*year/);
            const resumeYears = resumeYearsMatch ? parseInt(resumeYearsMatch[1]) : 0;
            
            const meetsExperience = resumeYears >= requiredYears;
            
            return {
                found: meetsExperience,
                explanation: meetsExperience ? 
                    `The candidate has ${resumeYears} years of experience, meeting the ${requiredYears}+ year requirement.` :
                    `The candidate has ${resumeYears} years of experience, which is less than the required ${requiredYears}+ years.`,
                excerpt: experienceSection || this.getResumeSnippet(resumeText, 400)
            };
        }
        
        // Look for specific technologies or skills
        const keywords = req.split(/[\s,]+/).filter(word => word.length > 2);
        let foundKeywords = 0;
        let foundExcerpts = [];
        
        keywords.forEach(keyword => {
            if (resumeLower.includes(keyword.toLowerCase())) {
                foundKeywords++;
                const snippet = this.findKeywordContext(resumeText, keyword);
                if (snippet) foundExcerpts.push(snippet);
            }
        });
        
        const skillsSection = this.extractSection(resumeText, ['skills', 'technical', 'technologies']);
        const isFound = foundKeywords > 0 || (skillsSection && skillsSection.toLowerCase().includes(req));
        
        return {
            found: isFound,
            explanation: isFound ? 
                `The requirement keywords are mentioned in the resume.` :
                `The specific requirement is not clearly mentioned or demonstrated.`,
            excerpt: foundExcerpts.length > 0 ? foundExcerpts.join('\n\n') : 
                    (skillsSection || this.getResumeSnippet(resumeText, 300))
        };
    }

    extractSection(resumeText, sectionNames) {
        const lines = resumeText.split('\n');
        let sectionStart = -1;
        let sectionEnd = -1;
        
        // Find section start - look for section headers like "🎓 EDUCATION & CERTIFICATIONS"
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].toLowerCase().trim();
            if (sectionNames.some(name => line.includes(name)) || 
                (sectionNames.includes('education') && (line.includes('🎓 education') || line.includes('education & certifications')))) {
                sectionStart = i;
                break;
            }
        }
        
        if (sectionStart === -1) return null;
        
        // Find section end (next major section with emojis or uppercase headers)
        for (let i = sectionStart + 1; i < lines.length; i++) {
            const line = lines[i].trim();
            // Look for next major section headers, but skip individual emoji lines within the section
            if (line.match(/^(💼.*EXPERIENCE|🎯.*OBJECTIVE|🛠.*SKILLS|📊.*PROJECTS|🏆.*ACHIEVEMENTS)/i) || 
                line.match(/^[A-Z\s&]{5,}$/) ||
                line.includes('════════')) {
                sectionEnd = i;
                break;
            }
        }
        
        if (sectionEnd === -1) sectionEnd = Math.min(sectionStart + 20, lines.length);
        
        // Get the section content, filtering out empty lines and including meaningful content
        const sectionLines = lines.slice(sectionStart, sectionEnd);
        const contentLines = sectionLines.filter((line, index) => {
            const trimmed = line.trim();
            // Keep header and any non-empty lines
            return trimmed.length > 0 && !(trimmed.match(/^[-=_]{3,}$/)); // Remove separator lines
        });
        
        return contentLines.join('\n').trim();
    }

    findKeywordContext(resumeText, keyword) {
        const lines = resumeText.split('\n');
        for (let i = 0; i < lines.length; i++) {
            if (lines[i].toLowerCase().includes(keyword.toLowerCase())) {
                // Return the line and a few lines around it for context
                const start = Math.max(0, i - 1);
                const end = Math.min(lines.length, i + 3);
                return lines.slice(start, end).join('\n');
            }
        }
        return null;
    }

    getResumeSnippet(resumeText, maxLength = 200) {
        if (!resumeText) return 'No content available.';
        
        // Get first meaningful content, skip headers
        const lines = resumeText.split('\n').filter(line => line.trim().length > 0);
        let content = '';
        
        for (let line of lines) {
            if (content.length + line.length > maxLength) break;
            content += line + '\n';
        }
        
        return content.trim() || 'Resume content not accessible.';
    }

    resetToInput() {
        const inputSection = document.querySelector('.input-section');
        const resultsSection = document.getElementById('resultsSection');
        const heroSection = document.querySelector('.hero');
        
        if (resultsSection) resultsSection.style.display = 'none';
        if (heroSection) heroSection.style.display = 'block';
        if (inputSection) {
            inputSection.style.display = 'block';
            // Smooth scroll to input
            inputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        // Clear previous results
        this.goodResume = '';
        this.badResume = '';

        // Restore page title
        document.title = '🎯 Resume Screening Assistant';

        // Focus on textarea
        setTimeout(() => {
            document.getElementById('jobDescription').focus();
        }, 500);
    }

    async copyResume(button) {
        const target = button.dataset.target;
        const content = target === 'good' ? this.goodResume : this.badResume;
        
        if (!content) {
            this.showToast('No content to copy', 'error');
            return;
        }

        try {
            await navigator.clipboard.writeText(content);
            this.showToast(`${target === 'good' ? 'Strong' : 'Weak'} candidate example copied to clipboard!`, 'success');
            
            // Visual feedback
            const originalIcon = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i>';
            button.style.background = 'var(--secondary-color)';
            button.style.color = 'white';
            
            setTimeout(() => {
                button.innerHTML = originalIcon;
                button.style.background = '';
                button.style.color = '';
            }, 2000);
            
        } catch (error) {
            console.error('Copy error:', error);
            this.showToast('Failed to copy to clipboard', 'error');
        }
    }

    downloadResume(button) {
        const target = button.dataset.target;
        const content = target === 'good' ? this.goodResume : this.badResume;
        const filename = target === 'good' ? 'strong_candidate_example.txt' : 'weak_candidate_example.txt';
        
        if (!content) {
            this.showToast('No content to download', 'error');
            return;
        }

        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showToast(`${filename} downloaded!`, 'success');
    }

    async exportPDFs() {
        if (!this.jobDescription) {
            this.showToast('No job description available for PDF export', 'error');
            return;
        }

        const exportBtn = document.getElementById('exportPdfBtn');
        const originalText = exportBtn.innerHTML;
        exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating PDFs...';
        exportBtn.disabled = true;

        try {
            const response = await fetch('/export/pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ job_description: this.jobDescription })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'PDF export failed');
            }

            // Download PDFs
            this.downloadBase64File(data.good_pdf, 'strong_candidate_example.pdf');
            this.downloadBase64File(data.bad_pdf, 'weak_candidate_example.pdf');

            this.showToast('PDFs exported successfully!', 'success');

        } catch (error) {
            console.error('PDF export error:', error);
            this.showToast(error.message || 'Failed to export PDFs', 'error');
        } finally {
            exportBtn.innerHTML = originalText;
            exportBtn.disabled = false;
        }
    }

    downloadBase64File(base64Data, filename) {
        const byteCharacters = atob(base64Data);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/pdf' });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        if (!toast) return;

        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.classList.add('show');

        // Auto hide after 4 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);

        // Manual hide on click
        toast.addEventListener('click', () => {
            toast.classList.remove('show');
        }, { once: true });
    }

    initializeModal() {
        const modal = document.getElementById('modal');
        const closeBtn = document.querySelector('.close');

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
}

// Global functions for modal content
function showAbout() {
    const modalBody = document.getElementById('modalBody');
    const modal = document.getElementById('modal');
    
    modalBody.innerHTML = `
        <h2>About Resume Screening Assistant</h2>
        <p>This AI-powered tool helps HR professionals and recruiters understand candidate quality by generating realistic resume examples based on your job postings.</p>
        
        <h3>How it works:</h3>
        <ul>
            <li>Paste your job posting or description</li>
            <li>AI analyzes requirements and industry context</li>
            <li>Generates two candidate resume examples: strong vs weak</li>
            <li>Use these examples to train your screening process</li>
        </ul>
        
        <h3>Perfect for:</h3>
        <ul>
            <li>Training new HR team members</li>
            <li>Standardizing screening criteria</li>
            <li>Understanding what quality candidates look like</li>
            <li>Creating screening benchmarks</li>
            <li>Improving recruitment processes</li>
        </ul>
    `;
    modal.style.display = 'block';
}

function showTips() {
    const modalBody = document.getElementById('modalBody');
    const modal = document.getElementById('modal');
    
    modalBody.innerHTML = `
        <h2>Resume Screening Tips</h2>
        
        <h3>🎯 What Strong Candidates Show:</h3>
        <ul>
            <li>Quantified achievements with specific metrics</li>
            <li>Direct alignment with job requirements</li>
            <li>Progressive career growth and responsibility</li>
            <li>Clear, professional formatting</li>
            <li>Relevant technical skills and certifications</li>
            <li>Industry-appropriate language and keywords</li>
            <li>Concrete examples of impact and results</li>
        </ul>
        
        <h3>🚩 Red Flags in Weak Candidates:</h3>
        <ul>
            <li>Generic, templated content</li>
            <li>Spelling and grammar errors</li>
            <li>Irrelevant or outdated experience</li>
            <li>Vague job descriptions without specifics</li>
            <li>Poor formatting or unprofessional presentation</li>
            <li>Missing key requirements from job posting</li>
            <li>Unexplained gaps or job-hopping patterns</li>
        </ul>
        
        <h3>💡 Screening Best Practices:</h3>
        <ul>
            <li>Use these examples to calibrate your team</li>
            <li>Create consistent evaluation criteria</li>
            <li>Focus on requirements alignment first</li>
            <li>Look for progression and growth patterns</li>
            <li>Test with different role types and seniority levels</li>
        </ul>
    `;
    modal.style.display = 'block';
}

// Functions for managing requirements
function addRequirement(containerId) {
    const container = document.getElementById(containerId);
    const newItem = document.createElement('div');
    newItem.className = 'requirement-item';
    
    const placeholder = containerId === 'nonNegotiables' ? 
        'e.g., New non-negotiable requirement' : 
        'e.g., New nice-to-have requirement';
    
    newItem.innerHTML = `
        <input type="text" class="requirement-input" placeholder="${placeholder}">
        <button type="button" class="remove-btn" onclick="removeRequirement(this)">×</button>
    `;
    
    // Insert before the add button
    container.appendChild(newItem);
    
    // Focus on the new input
    newItem.querySelector('.requirement-input').focus();
}

function removeRequirement(button) {
    const item = button.parentElement;
    const container = item.parentElement;
    
    // Don't allow removing if it's the last item in non-negotiables
    if (container.id === 'nonNegotiables' && container.children.length <= 1) {
        // Show a toast message instead
        const app = window.resumeApp;
        if (app && app.showToast) {
            app.showToast('Must have at least one non-negotiable requirement', 'error');
        }
        return;
    }
    
    item.remove();
}

// Global function to close examples modal
function closeExamplesModal() {
    const modal = document.getElementById('examplesModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.resumeApp = new ResumeGenerator();
    
    // Add click handler for examples modal backdrop
    const examplesModal = document.getElementById('examplesModal');
    if (examplesModal) {
        examplesModal.addEventListener('click', (e) => {
            if (e.target === examplesModal) {
                closeExamplesModal();
            }
        });
    }
});

// Add some nice visual effects
document.addEventListener('mousemove', (e) => {
    if (window.innerWidth > 768) {
        const cursor = document.querySelector('.cursor');
        if (!cursor) {
            const newCursor = document.createElement('div');
            newCursor.className = 'cursor';
            newCursor.style.cssText = `
                position: fixed;
                width: 20px;
                height: 20px;
                background: radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%);
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                transition: transform 0.1s ease;
            `;
            document.body.appendChild(newCursor);
        }
        
        const cursorElement = document.querySelector('.cursor');
        if (cursorElement) {
            cursorElement.style.left = e.clientX - 10 + 'px';
            cursorElement.style.top = e.clientY - 10 + 'px';
        }
    }
});