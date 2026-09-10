(function () {
	'use strict';

	class DCTTestimonialsSlider {
		constructor(root) {
			this.root = root;
			this.track = root.querySelector('.dct-testimonials-slider__track');
			this.slides = Array.from(root.querySelectorAll('.dct-testimonials-slider__slide'));
			this.previousButton = root.querySelector('.dct-testimonials-slider__arrow--previous');
			this.nextButton = root.querySelector('.dct-testimonials-slider__arrow--next');
			this.dots = Array.from(root.querySelectorAll('.dct-testimonials-slider__dot'));
			this.status = root.querySelector('.dct-testimonials-slider__status');
			this.currentIndex = 0;
			this.timer = null;
			this.touchStartX = 0;
			this.touchStartY = 0;
			this.pauseReasons = new Set();
			this.loop = root.dataset.loop === 'yes';
			this.pauseOnHover = root.dataset.pauseHover === 'yes';
			this.interval = this.normalizeInterval(root.dataset.interval);
			this.statusTemplate = root.dataset.statusTemplate || 'Depoimento %1$d de %2$d';
			this.autoplayEnabled = root.dataset.autoplay === 'yes' && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

			if (!this.track || this.slides.length === 0) {
				return;
			}

			this.root.dataset.dctInitialized = 'yes';
			this.bindEvents();
			this.setupVisibilityObserver();
			this.update(false);

			if (this.slides.length < 2) {
				this.root.classList.add('is-single');
				this.autoplayEnabled = false;
			}

			this.startAutoplay();
		}

		normalizeInterval(value) {
			const parsed = Number.parseInt(value, 10);

			if (!Number.isFinite(parsed)) {
				return 6000;
			}

			return Math.min(60000, Math.max(1000, parsed));
		}

		bindEvents() {
			if (this.previousButton) {
				this.previousButton.addEventListener('click', () => this.goTo(this.currentIndex - 1, true));
			}

			if (this.nextButton) {
				this.nextButton.addEventListener('click', () => this.goTo(this.currentIndex + 1, true));
			}

			this.dots.forEach((dot) => {
				dot.addEventListener('click', () => {
					const index = Number.parseInt(dot.dataset.slide, 10);

					if (Number.isFinite(index)) {
						this.goTo(index, true);
					}
				});
			});

			this.root.addEventListener('keydown', (event) => {
				if (event.target.matches('input, textarea, select')) {
					return;
				}

				if (event.key === 'ArrowLeft') {
					event.preventDefault();
					this.goTo(this.currentIndex - 1, true);
				}

				if (event.key === 'ArrowRight') {
					event.preventDefault();
					this.goTo(this.currentIndex + 1, true);
				}
			});

			if (this.pauseOnHover) {
				this.root.addEventListener('mouseenter', () => this.pause('hover'));
				this.root.addEventListener('mouseleave', () => this.resume('hover'));
			}

			this.root.addEventListener('focusin', () => this.pause('focus'));
			this.root.addEventListener('focusout', (event) => {
				if (!this.root.contains(event.relatedTarget)) {
					this.resume('focus');
				}
			});

			this.root.addEventListener('touchstart', (event) => {
				if (!event.changedTouches.length) {
					return;
				}

				this.touchStartX = event.changedTouches[0].clientX;
				this.touchStartY = event.changedTouches[0].clientY;
			}, { passive: true });

			this.root.addEventListener('touchend', (event) => {
				if (!event.changedTouches.length) {
					return;
				}

				const deltaX = event.changedTouches[0].clientX - this.touchStartX;
				const deltaY = event.changedTouches[0].clientY - this.touchStartY;

				if (Math.abs(deltaX) > 50 && Math.abs(deltaX) > Math.abs(deltaY)) {
					this.goTo(this.currentIndex + (deltaX < 0 ? 1 : -1), true);
				}
			}, { passive: true });

			document.addEventListener('visibilitychange', () => {
				if (document.hidden) {
					this.pause('document-hidden');
				} else {
					this.resume('document-hidden');
				}
			});
		}

		setupVisibilityObserver() {
			if (!('IntersectionObserver' in window)) {
				return;
			}

			this.observer = new IntersectionObserver((entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						this.resume('outside-viewport');
					} else {
						this.pause('outside-viewport');
					}
				});
			}, { threshold: 0.1 });

			this.observer.observe(this.root);
		}

		goTo(targetIndex, userInitiated) {
			let nextIndex = targetIndex;

			if (this.loop) {
				nextIndex = (targetIndex + this.slides.length) % this.slides.length;
			} else {
				nextIndex = Math.max(0, Math.min(this.slides.length - 1, targetIndex));
			}

			if (nextIndex === this.currentIndex && this.slides.length > 1) {
				this.resetAutoplay();
				return;
			}

			this.currentIndex = nextIndex;
			this.update(userInitiated);
			this.resetAutoplay();
		}

		update(announce) {
			this.track.style.transform = `translate3d(-${this.currentIndex * 100}%, 0, 0)`;

			this.slides.forEach((slide, index) => {
				const active = index === this.currentIndex;
				slide.classList.toggle('is-active', active);
				slide.setAttribute('aria-hidden', active ? 'false' : 'true');
			});

			this.dots.forEach((dot, index) => {
				const active = index === this.currentIndex;
				dot.classList.toggle('is-active', active);
				dot.setAttribute('aria-current', active ? 'true' : 'false');
			});

			if (!this.loop) {
				this.setButtonState(this.previousButton, this.currentIndex === 0);
				this.setButtonState(this.nextButton, this.currentIndex === this.slides.length - 1);
			}

			if (announce && this.status) {
				this.status.textContent = this.statusTemplate
					.replace('%1$d', String(this.currentIndex + 1))
					.replace('%2$d', String(this.slides.length));
			}
		}

		setButtonState(button, disabled) {
			if (!button) {
				return;
			}

			button.disabled = disabled;
			button.setAttribute('aria-disabled', disabled ? 'true' : 'false');
		}

		pause(reason) {
			this.pauseReasons.add(reason);
			this.stopAutoplay();
		}

		resume(reason) {
			this.pauseReasons.delete(reason);
			this.startAutoplay();
		}

		startAutoplay() {
			if (!this.autoplayEnabled || this.pauseReasons.size > 0 || this.timer || this.slides.length < 2) {
				return;
			}

			this.timer = window.setInterval(() => {
				if (!document.documentElement.contains(this.root)) {
					this.stopAutoplay();
					if (this.observer) {
						this.observer.disconnect();
					}
					return;
				}

				const nextIndex = this.currentIndex + 1;

				if (!this.loop && nextIndex >= this.slides.length) {
					this.stopAutoplay();
					return;
				}

				this.goTo(nextIndex, false);
			}, this.interval);
		}

		stopAutoplay() {
			if (!this.timer) {
				return;
			}

			window.clearInterval(this.timer);
			this.timer = null;
		}

		resetAutoplay() {
			this.stopAutoplay();
			this.startAutoplay();
		}
	}

	function initializeSlider(root) {
		if (!root || root.dataset.dctInitialized === 'yes') {
			return;
		}

		root.dctTestimonialsSlider = new DCTTestimonialsSlider(root);
	}

	function initializeWithin(scope) {
		const element = scope && scope.jquery ? scope[0] : scope;

		if (!element) {
			return;
		}

		if (element.matches && element.matches('.dct-testimonials-slider')) {
			initializeSlider(element);
		}

		if (element.querySelectorAll) {
			element.querySelectorAll('.dct-testimonials-slider').forEach(initializeSlider);
		}
	}

	function initializeDocument() {
		document.querySelectorAll('.dct-testimonials-slider').forEach(initializeSlider);
	}

	let elementorHookRegistered = false;

	function registerElementorHook() {
		if (elementorHookRegistered || !window.elementorFrontend || !window.elementorFrontend.hooks) {
			return;
		}

		window.elementorFrontend.hooks.addAction(
			'frontend/element_ready/dct_testimonials_slider.default',
			(scope) => initializeWithin(scope)
		);

		elementorHookRegistered = true;
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', initializeDocument, { once: true });
	} else {
		initializeDocument();
	}

	window.addEventListener('elementor/frontend/init', registerElementorHook);
	registerElementorHook();
}());
