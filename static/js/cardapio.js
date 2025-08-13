/**
 * CARDAPIO.JS - JavaScript para pagina de cardapio
 * Funcionalidades: Modal de imagens, navegacao suave, animacoes e filtros
 * VERSAO CORRIGIDA - Modal funcionando perfeitamente
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ===============================================
    // CONFIGURACOES GLOBAIS
    // ===============================================
    
    const CONFIG = {
        scrollOffset: 100,
        scrollDuration: 600,
        modalFadeTime: 300,
        activeClass: 'active',
        imagePath: '/static/images/cardapio/'
    };
    
    // ===============================================
    // ELEMENTOS DO DOM
    // ===============================================
    
    const menuNavLinks = document.querySelectorAll('.menu-nav .nav-link');
    const sections = document.querySelectorAll('.categoria-section');
    const btnPedirFixo = document.querySelector('.btn-pedir-fixo');
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalContent = document.querySelector('.modal-content');
    const modalClose = document.querySelector('.modal-close');
    const itemCards = document.querySelectorAll('.item-card');
    
    // ===============================================
    // FUNCIONALIDADE DE MODAL DE IMAGENS - CORRIGIDA
    // ===============================================
    
    /**
     * Abre o modal com a imagem do item selecionado
     * @param {string} itemId - ID do item para buscar a imagem correspondente
     */
    window.openModal = function(itemId) {
        if (!modal || !modalImage) {
            console.error('Elementos do modal nao encontrados');
            return;
        }

        // Encontrar a imagem original clicada para pegar o src correto
        const clickedImage = findOriginalImage(itemId);
        let imageSrc = '';

        if (clickedImage && clickedImage.src && !clickedImage.src.includes('placeholder')) {
            // Usar a mesma imagem que esta sendo exibida na miniatura
            imageSrc = clickedImage.src;
        } else {
            // Fallback: tentar construir o caminho baseado no itemId
            imageSrc = `${CONFIG.imagePath}${itemId}.jpg`;
        }

        // Configurar a imagem do modal
        modalImage.src = imageSrc;
        modalImage.alt = `Imagem ampliada - ${itemId}`;
        
        // Mostrar o modal com as classes corretas
        modal.style.display = 'flex';
        
        // Pequeno delay para permitir que o display seja aplicado antes da animacao
        setTimeout(() => {
            modal.classList.add('active');
        }, 10);
        
        // Adicionar listener para tecla ESC
        document.addEventListener('keydown', handleModalKeydown);
        
        // Impedir scroll da pagina
        document.body.style.overflow = 'hidden';
        
        // Tratamento de erro para imagem nao encontrada
        modalImage.onerror = function() {
            // Tentar outras extensões
            tryAlternativeFormats(this, itemId);
        };
    };

    /**
     * Encontra a imagem original que foi clicada
     */
    function findOriginalImage(itemId) {
        // Procurar por elementos com onclick que contem o itemId
        const clickableElements = document.querySelectorAll('[onclick*="' + itemId + '"]');
        
        for (let element of clickableElements) {
            // Se for um container de imagem, procurar a img dentro dele
            const img = element.querySelector('img');
            if (img) {
                return img;
            }
            // Se o proprio elemento for uma imagem
            if (element.tagName === 'IMG') {
                return element;
            }
        }
        
        return null;
    }

    /**
     * Tenta formatos alternativos de imagem
     */
    function tryAlternativeFormats(imgElement, itemId) {
        const formats = ['png', 'webp', 'svg'];
        let currentFormat = 0;
        
        function tryNextFormat() {
            if (currentFormat >= formats.length) {
                // Usar placeholder final
                imgElement.src = `${CONFIG.imagePath}placeholder.svg`;
                imgElement.alt = 'Imagem nao disponivel';
                return;
            }
            
            const newSrc = `${CONFIG.imagePath}${itemId}.${formats[currentFormat]}`;
            imgElement.onerror = function() {
                currentFormat++;
                tryNextFormat();
            };
            imgElement.src = newSrc;
        }
        
        tryNextFormat();
    }
    
    /**
     * Fecha o modal de imagem
     */
    window.closeModal = function() {
        if (!modal) return;
        
        // Adicionar classe de fechamento para animacao
        modal.classList.add('closing');
        modal.classList.remove('active');
        
        // Remover listeners
        document.removeEventListener('keydown', handleModalKeydown);
        
        // Restaurar scroll da pagina apos a animacao
        setTimeout(() => {
            modal.style.display = 'none';
            modal.classList.remove('closing');
            document.body.style.overflow = 'auto';
        }, CONFIG.modalFadeTime);
    };
    
    /**
     * Handler para teclas no modal
     */
    function handleModalKeydown(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
    }
    
    // Event listeners para o modal
    if (modal) {
        // Fechar ao clicar no overlay
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    
    if (modalContent) {
        // Impedir que cliques no conteudo fechem o modal
        modalContent.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }
    
    if (modalClose) {
        // Fechar ao clicar no botao X
        modalClose.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            closeModal();
        });
    }
    
    // ===============================================
    // NAVEGACAO SUAVE
    // ===============================================
    
    function initSmoothScrolling() {
        menuNavLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);
                
                if (targetElement) {
                    smoothScrollTo(targetElement);
                    
                    // Atualiza URL sem recarregar a pagina
                    history.pushState(null, null, targetId);
                    
                    // Atualiza links ativos
                    menuNavLinks.forEach(navLink => {
                        navLink.classList.remove(CONFIG.activeClass);
                    });
                    this.classList.add(CONFIG.activeClass);
                }
            });
        });
    }
    
    function smoothScrollTo(element) {
        const targetPosition = element.getBoundingClientRect().top + window.pageYOffset - CONFIG.scrollOffset;
        
        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
        });
    }
    
    // ===============================================
    // ANIMACOES DE ENTRADA
    // ===============================================
    
    function initEntryAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        itemCards.forEach((card, index) => {
            card.classList.add('animate-entry');
            card.style.transitionDelay = `${index * 0.05}s`;
            observer.observe(card);
        });
    }
    
    // ===============================================
    // FILTRO DE BUSCA
    // ===============================================
    
    function initSearchFilter() {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container mb-4';
        searchContainer.innerHTML = `
            <div class="input-group">
                <input type="text" class="form-control" id="searchCardapio" placeholder="Buscar no cardapio...">
                <button class="btn btn-outline-secondary" type="button" id="clearSearch">
                    <i class="bi bi-x-circle"></i>
                </button>
            </div>
        `;
        
        const firstSection = document.querySelector('.categoria-section');
        if (firstSection && firstSection.parentNode) {
            firstSection.parentNode.insertBefore(searchContainer, firstSection);
        }
        
        const searchInput = document.getElementById('searchCardapio');
        const clearButton = document.getElementById('clearSearch');
        
        if (searchInput) {
            searchInput.addEventListener('input', filterItems);
        }
        if (clearButton) {
            clearButton.addEventListener('click', clearSearch);
        }
        
        function filterItems() {
            const searchTerm = searchInput.value.toLowerCase().trim();
            let hasResults = false;
            
            document.querySelectorAll('.categoria-section').forEach(section => {
                section.style.display = 'none';
            });
            
            itemCards.forEach(card => {
                const itemName = card.querySelector('.item-nome');
                if (itemName) {
                    const matchesSearch = itemName.textContent.toLowerCase().includes(searchTerm);
                    card.style.display = matchesSearch || searchTerm === '' ? 'block' : 'none';
                    
                    if (matchesSearch && searchTerm !== '') {
                        let section = card.closest('.categoria-section');
                        if (section) {
                            section.style.display = 'block';
                            hasResults = true;
                        }
                    }
                }
            });
            
            if (searchTerm === '') {
                document.querySelectorAll('.categoria-section').forEach(section => {
                    section.style.display = 'block';
                });
                hasResults = true;
            }
            
            // Gerenciar mensagem de "nenhum resultado"
            let noResultsMsg = document.getElementById('noResultsMessage');
            if (!hasResults) {
                if (!noResultsMsg) {
                    noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'noResultsMessage';
                    noResultsMsg.className = 'alert alert-info text-center my-4';
                    searchContainer.after(noResultsMsg);
                }
                noResultsMsg.innerHTML = `
                    <i class="bi bi-emoji-frown me-2"></i>
                    Nenhum item encontrado para "${searchTerm}"
                `;
                noResultsMsg.style.display = 'block';
            } else if (noResultsMsg) {
                noResultsMsg.style.display = 'none';
            }
        }
        
        function clearSearch() {
            searchInput.value = '';
            filterItems();
            searchInput.focus();
        }
    }
    
    // ===============================================
    // BOTAO FLUTUANTE DE PEDIDO
    // ===============================================
    
    function initFloatingButton() {
        if (!btnPedirFixo) return;
        
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                btnPedirFixo.classList.add('visible');
            } else {
                btnPedirFixo.classList.remove('visible');
            }
            
            const footer = document.querySelector('footer');
            if (footer) {
                const footerRect = footer.getBoundingClientRect();
                if (footerRect.top < window.innerHeight) {
                    const overlap = window.innerHeight - footerRect.top;
                    btnPedirFixo.style.bottom = `${Math.min(overlap + 20, 100)}px`;
                } else {
                    btnPedirFixo.style.bottom = '20px';
                }
            }
        });
    }
    
    // ===============================================
    // INICIALIZACAO DE MINIATURAS - CORRIGIDA
    // ===============================================
    
    function initThumbnails() {
        // Procurar por todos os containers de imagem que têm onclick
        const imageContainers = document.querySelectorAll('.item-image-container[onclick]');
        
        imageContainers.forEach(container => {
            const onclickAttr = container.getAttribute('onclick');
            if (!onclickAttr) return;
            
            // Extrair o itemId do atributo onclick
            const match = onclickAttr.match(/openModal\(['"]([^'"]*)['"]\)/);
            if (!match || !match[1]) return;
            
            const itemId = match[1];
            
            // Verificar se ja existe uma imagem no container
            const existingImg = container.querySelector('img.item-image');
            if (existingImg && existingImg.src && !existingImg.src.includes('placeholder')) {
                // Ja tem uma imagem valida, nao fazer nada
                return;
            }
            
            // Tentar carregar miniatura para containers que sao placeholders
            if (container.classList.contains('item-image-placeholder')) {
                loadThumbnail(container, itemId);
            }
        });
    }
    
    function loadThumbnail(placeholder, itemId) {
        const extensions = ['jpg', 'png', 'webp'];
        let currentExtension = 0;
        
        function tryLoadImage() {
            if (currentExtension >= extensions.length) {
                // Manter o placeholder original se todas falharem
                return;
            }
            
            const ext = extensions[currentExtension];
            const thumbnailPath = `${CONFIG.imagePath}${itemId}.${ext}`;
            
            const img = document.createElement('img');
            img.className = 'item-thumbnail';
            img.alt = `Miniatura de ${itemId}`;
            img.src = thumbnailPath;
            
            img.onload = function() {
                // Limpar conteudo do placeholder e adicionar imagem
                placeholder.innerHTML = '';
                placeholder.appendChild(img);
                placeholder.classList.add('has-image');
            };
            
            img.onerror = function() {
                currentExtension++;
                tryLoadImage();
            };
        }
        
        tryLoadImage();
    }
    
    // ===============================================
    // MELHORAR CLIQUES NAS IMAGENS
    // ===============================================
    
    function initImageClicks() {
        // Adicionar event listeners para todos os elementos clicaveis do cardapio
        const clickableElements = document.querySelectorAll('[onclick*="openModal"]');
        
        clickableElements.forEach(element => {
            // Adicionar cursor pointer se nao tiver
            if (window.getComputedStyle(element).cursor === 'auto') {
                element.style.cursor = 'pointer';
            }
            
            // Melhorar feedback visual no hover
            element.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.02)';
            });
            
            element.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }
    
    // ===============================================
    // NAVEGACAO POR CATEGORIAS - MELHORADA
    // ===============================================
    
    function initCategoryNavigation() {
        // Atualizar link ativo baseado na secao visivel
        const observerOptions = {
            threshold: 0.3,
            rootMargin: '-140px 0px -50% 0px'
        };
        
        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const sectionId = entry.target.id;
                    updateActiveNavLink(sectionId);
                }
            });
        }, observerOptions);
        
        sections.forEach(section => {
            sectionObserver.observe(section);
        });
    }
    
    function updateActiveNavLink(activeSectionId) {
        menuNavLinks.forEach(link => {
            link.classList.remove(CONFIG.activeClass);
            if (link.getAttribute('href') === `#${activeSectionId}`) {
                link.classList.add(CONFIG.activeClass);
            }
        });
    }
    
    // ===============================================
    // INICIALIZACAO PRINCIPAL
    // ===============================================
    
    // Inicializar todas as funcionalidades
    initSmoothScrolling();
    initEntryAnimations();
    initSearchFilter();
    initFloatingButton();
    initThumbnails();
    initImageClicks();
    initCategoryNavigation();
    
    // Verificar hash na URL para scroll inicial
    if (window.location.hash) {
        setTimeout(() => {
            const targetElement = document.querySelector(window.location.hash);
            if (targetElement) {
                smoothScrollTo(targetElement);
            }
        }, 500);
    }
    
    // ===============================================
    // DEBUG E LOGS
    // ===============================================
    
    console.log('??? Cardapio JS inicializado com sucesso!');
    console.log('?? Modal de imagens configurado');
    console.log('?? Sistema de busca ativo');
    console.log('?? Responsividade aplicada');
    
    // Log para debug do modal
    if (!modal) console.warn('?? Elemento #imageModal nao encontrado');
    if (!modalImage) console.warn('?? Elemento #modalImage nao encontrado');
    if (!modalContent) console.warn('?? Elemento .modal-content nao encontrado');
});