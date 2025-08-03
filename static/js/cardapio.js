/**
 * CARDAPIO.JS - JavaScript para pagina de cardapio
 * Funcionalidades: Scrollspy, rolagem suave, animacoes
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ===============================================
    // CONFIGURACOES GLOBAIS
    // ===============================================
    
    const CONFIG = {
        scrollOffset: 140, // Offset para compensar navbar fixa
        scrollDuration: 800, // Duracao da animacao de scroll
        throttleDelay: 16, // Delay para throttle (60fps)
        activeClass: 'active'
    };
    
    // ===============================================
    // ELEMENTOS DO DOM
    // ===============================================
    
    const menuNavLinks = document.querySelectorAll('.menu-nav .nav-link');
    const sections = document.querySelectorAll('.categoria-section');
    const btnPedirFixo = document.querySelector('.btn-pedir-fixo');
    
    // ===============================================
    // UTILITARIOS
    // ===============================================
    
    /**
     * Throttle function para otimizar performance
     */
    function throttle(func, delay) {
        let timeoutId;
        let lastExecTime = 0;
        return function(...args) {
            const currentTime = Date.now();
            
            if (currentTime - lastExecTime > delay) {
                func.apply(this, args);
                lastExecTime = currentTime;
            } else {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    func.apply(this, args);
                    lastExecTime = Date.now();
                }, delay - (currentTime - lastExecTime));
            }
        };
    }
    
    /**
     * Smooth scroll para elemento
     */
    function smoothScrollTo(targetPosition, duration = CONFIG.scrollDuration) {
        const startPosition = window.pageYOffset;
        const distance = targetPosition - startPosition;
        let startTime = null;
        
        function animation(currentTime) {
            if (startTime === null) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);
            
            // Easing function (easeInOutCubic)
            const ease = progress < 0.5 
                ? 4 * progress * progress * progress 
                : (progress - 1) * (2 * progress - 2) * (2 * progress - 2) + 1;
            
            window.scrollTo(0, startPosition + distance * ease);
            
            if (timeElapsed < duration) {
                requestAnimationFrame(animation);
            }
        }
        
        requestAnimationFrame(animation);
    }
    
    /**
     * Obter posicao do elemento com offset
     */
    function getElementPosition(element) {
        const rect = element.getBoundingClientRect();
        return rect.top + window.pageYOffset - CONFIG.scrollOffset;
    }
    
    // ===============================================
    // SCROLLSPY FUNCTIONALITY
    // ===============================================
    
    /**
     * Atualiza link ativo baseado na posicao do scroll
     */
    function updateActiveLink() {
        const scrollPosition = window.pageYOffset + CONFIG.scrollOffset + 50;
        let activeSection = null;
        
        // Encontra a secao ativa
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionBottom = sectionTop + section.offsetHeight;
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                activeSection = section;
            }
        });
        
        // Se nenhuma secao especifica, usa a primeira se estivermos no topo
        if (!activeSection && window.pageYOffset < 200) {
            activeSection = sections[0];
        }
        
        // Atualiza classes dos links
        menuNavLinks.forEach(link => {
            link.classList.remove(CONFIG.activeClass);
            
            if (activeSection) {
                const href = link.getAttribute('href');
                const sectionId = '#' + activeSection.id;
                
                if (href === sectionId) {
                    link.classList.add(CONFIG.activeClass);
                }
            }
        });
    }
    
    // ===============================================
    // NAVEGACAO SUAVE
    // ===============================================
    
    /**
     * Adiciona event listeners para navegacao suave
     */
    function initSmoothScrolling() {
        menuNavLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    const targetPosition = getElementPosition(targetElement);
                    smoothScrollTo(targetPosition);
                    
                    // Atualiza URL sem trigger do scroll
                    history.pushState(null, null, targetId);
                    
                    // Remove foco do link apos clique (mobile)
                    this.blur();
                }
            });
        });
    }
    
    // ===============================================
    // ANIMACOES DO BOTAO FIXO
    // ===============================================
    
    /**
     * Controla visibilidade do botao fixo
     */
    function handleFixedButton() {
        const scrollPosition = window.pageYOffset;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;
        
        // Mostra botao apos rolar um pouco
        if (scrollPosition > 300) {
            btnPedirFixo.style.opacity = '1';
            btnPedirFixo.style.transform = 'translateY(0)';
        } else {
            btnPedirFixo.style.opacity = '0';
            btnPedirFixo.style.transform = 'translateY(20px)';
        }
        
        // Ajusta posicao no final da pagina para nao sobrepor footer
        const distanceFromBottom = documentHeight - (scrollPosition + windowHeight);
        if (distanceFromBottom < 100) {
            btnPedirFixo.style.transform = `translateY(-${100 - distanceFromBottom}px)`;
        }
    }
    
    // ===============================================
    // ANIMACOES DE ENTRADA
    // ===============================================
    
    /**
     * Adiciona animacoes aos cards quando entram na viewport
     */
    function initScrollAnimations() {
        const itemCards = document.querySelectorAll('.item-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        itemCards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    }
    
    // ===============================================
    // NAVEGACAO HORIZONTAL TOUCH (MOBILE)
    // ===============================================
    
    /**
     * Melhora navegacao horizontal em dispositivos touch
     */
    function initTouchNavigation() {
        const menuNav = document.querySelector('.menu-nav .nav');
        if (!menuNav) return;
        
        let isScrolling = false;
        let startX = 0;
        let scrollLeft = 0;
        
        menuNav.addEventListener('touchstart', (e) => {
            isScrolling = true;
            startX = e.touches[0].pageX - menuNav.offsetLeft;
            scrollLeft = menuNav.scrollLeft;
        });
        
        menuNav.addEventListener('touchmove', (e) => {
            if (!isScrolling) return;
            e.preventDefault();
            const x = e.touches[0].pageX - menuNav.offsetLeft;
            const walk = (x - startX) * 2;
            menuNav.scrollLeft = scrollLeft - walk;
        });
        
        menuNav.addEventListener('touchend', () => {
            isScrolling = false;
        });
    }
    
    // ===============================================
    // OTIMIZACOES DE PERFORMANCE
    // ===============================================
    
    /**
     * Throttled scroll handler
     */
    const handleScroll = throttle(() => {
        updateActiveLink();
        handleFixedButton();
    }, CONFIG.throttleDelay);
    
    /**
     * Debounced resize handler
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    const handleResize = debounce(() => {
        updateActiveLink();
    }, 250);
    
    // ===============================================
    // INICIALIZACAO
    // ===============================================
    
    /**
     * Inicializa todas as funcionalidades
     */
    function init() {
        // Configuracoes iniciais do botao fixo
        if (btnPedirFixo) {
            btnPedirFixo.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            btnPedirFixo.style.opacity = '0';
            btnPedirFixo.style.transform = 'translateY(20px)';
        }
        
        // Inicializa funcionalidades
        initSmoothScrolling();
        initScrollAnimations();
        initTouchNavigation();
        
        // Event listeners
        window.addEventListener('scroll', handleScroll, { passive: true });
        window.addEventListener('resize', handleResize);
        
        // Scroll inicial se ha hash na URL
        if (window.location.hash) {
            setTimeout(() => {
                const targetElement = document.querySelector(window.location.hash);
                if (targetElement) {
                    const targetPosition = getElementPosition(targetElement);
                    smoothScrollTo(targetPosition, 1000);
                }
            }, 100);
        }
        
        // Primeira verificacao
        updateActiveLink();
        handleFixedButton();
        
        console.log('Cardapio JS inicializado com sucesso!');
    }
    
    // ===============================================
    // HANDLERS DE EVENTOS ESPECIAIS
    // ===============================================
    
    /**
     * Handler para mudancas de orientacao (mobile)
     */
    window.addEventListener('orientationchange', function() {
        setTimeout(() => {
            updateActiveLink();
            handleFixedButton();
        }, 100);
    });
    
    /**
     * Handler para voltar/avancar do navegador
     */
    window.addEventListener('popstate', function() {
        if (window.location.hash) {
            const targetElement = document.querySelector(window.location.hash);
            if (targetElement) {
                const targetPosition = getElementPosition(targetElement);
                smoothScrollTo(targetPosition);
            }
        }
    });
    
    /**
     * Handler para teclas de atalho
     */
    document.addEventListener('keydown', function(e) {
        // Esc para voltar ao topo
        if (e.key === 'Escape') {
            smoothScrollTo(0);
        }
        
        // Setas para navegar entre secoes
        if (e.key === 'ArrowDown' && e.ctrlKey) {
            e.preventDefault();
            const activeLink = document.querySelector('.menu-nav .nav-link.active');
            const nextLink = activeLink ? activeLink.parentElement.nextElementSibling?.querySelector('.nav-link') : menuNavLinks[0];
            if (nextLink) nextLink.click();
        }
        
        if (e.key === 'ArrowUp' && e.ctrlKey) {
            e.preventDefault();
            const activeLink = document.querySelector('.menu-nav .nav-link.active');
            const prevLink = activeLink ? activeLink.parentElement.previousElementSibling?.querySelector('.nav-link') : null;
            if (prevLink) prevLink.click();
        }
    });
    
    // Inicializa quando DOM estiver pronto
    init();
});

// ===============================================
// UTILITIES GLOBAIS (se necessario)
// ===============================================

/**
 * Funcao global para scroll suave (pode ser chamada externamente)
 */
window.scrollToSection = function(sectionId) {
    const targetElement = document.querySelector(sectionId);
    if (targetElement) {
        const targetPosition = targetElement.offsetTop - 140;
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
};