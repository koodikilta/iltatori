<script lang="ts">
    import { onMount } from 'svelte';
    import { fly, fade, slide } from 'svelte/transition';
    import { Brain, CircleX, LogIn, User, LogOut, MessageCircle, Filter, FilterX, FileText } from 'lucide-svelte';
    import Notifications from '$lib/overlays/NotificationsOverlay.svelte';
    import Favorites from '$lib/overlays/FavoritesOverlay.svelte';
    import Sales from '$lib/overlays/SalesOverlay.svelte';
    import Messages from '$lib/overlays/MessagesOverlay.svelte';
    import Profile from '$lib/overlays/SalesOverlay.svelte';
    import FilterSelector from '$lib/components/ui/FilterSelector.svelte';
    import { goto } from '$app/navigation';
    import "../app.css";  // Make sure this is at the top

    let activeLink = '/'; 
    let overlayState = {
        notifications: false,
        favorites: false,
        sales: false,
        messages: false,
        profile: false
    };
    let showFilterSelector = false;

    function toggleOverlay(overlayName: keyof typeof overlayState) {
        if (overlayName === 'messages') {
            overlayState.messages = !overlayState.messages;
        } else {
            overlayState = {
                notifications: false,
                favorites: false,
                sales: false,
                profile: false,
                messages: overlayState.messages,
                [overlayName]: !overlayState[overlayName]
            };
        }
        activeLink = overlayName;
    }

    function navigateToOffers() {
        goto('/offers');
        activeLink = 'offers';
    }
</script>

<div class="app-container">
    <header>
        <h1>
            Iltatori
        </h1>
        <button class="toggle-filter" on:click={() => showFilterSelector = !showFilterSelector}>
            {#if showFilterSelector}
                <FilterX size={20} />
                Hide
            {:else}
                <Filter size={20} />
                Filters
            {/if}
        </button>
        <div class="search-bar">
            <input type="text" placeholder="Hae...">
        </div>
        <div class="nav-links" transition:fly={{ y: 50, duration: 300 }}>
            <button class="nav-link" class:active={activeLink === 'offers'} on:click={navigateToOffers}>
                <FileText size={20} />
                Tarjoukset
            </button>
            <button class="nav-link" class:active={activeLink === 'notifications'} on:click={() => toggleOverlay('notifications')}>
                <Brain size={20} />
                Hälytykset
            </button>
            <button class="nav-link" class:active={activeLink === 'favorites'} on:click={() => toggleOverlay('favorites')}>
                <Brain size={20} />
                Suosikit
            </button>
            <button class="nav-link" class:active={activeLink === 'sales'} on:click={() => toggleOverlay('sales')}>
                <Brain size={20} />
                Myynnit
            </button>
            <button class="nav-link" class:active={activeLink === 'profile'} on:click={() => toggleOverlay('profile')}>
                <User size={20} />
                Oma
            </button>
            <button class="nav-link" class:active={activeLink === 'messages'} on:click={() => toggleOverlay('messages')}>
                <MessageCircle size={20} />
                Viestit
            </button>
        </div>
    </header>




    <main>
        <slot />
    </main>
	<footer>
	</footer>
  </div>

  <div class="overlays-container" class:messages-open={overlayState.messages}>
    {#each Object.entries(overlayState) as [overlayName, isVisible]}
        {#if isVisible && overlayName !== 'messages'}
            <div class="overlay" transition:slide={{duration: 300}} on:click|self={() => toggleOverlay(overlayName)}>
                <div class="content" transition:fly={{y: 500, duration: 300}}>
                    {#if overlayName === 'notifications'}
                        <Notifications />
                    {:else if overlayName === 'favorites'}
                        <Favorites />
                    {:else if overlayName === 'sales'}
                        <Sales />
                    {:else if overlayName === 'profile'}
                        <Profile />
                    {/if}
                    <button class="close-button" on:click={() => toggleOverlay(overlayName)}>
                        <CircleX size={30} />

                    </button>
                </div>
            </div>
        {/if}
    {/each}
</div>

{#if overlayState.messages}
    <div class="messages-sidenav" transition:fly={{ x: 50, duration: 300 }}>
        <Messages />
        <button class="close-button" on:click={() => toggleOverlay('messages')}>
            <CircleX size={20} />
        </button>
    </div>
{/if}

{#if showFilterSelector}
<div class="filter-overlay" transition:fly={{ x: -250, duration: 300 }}>
    <FilterSelector />
</div>
{/if}

  <style>
    /* :global(.loading-spinner) {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 9999;
    } */
	.app-container {
	  display: flex;
	  flex-direction: column;
      position: absolute;
      top: 60px;
	  /* justify-content: center; */
	  /* align-items: center; */
	  overflow: hidden;
	  /* height: 100vh; */
	  /* width: 100vw; */;
	}

    
    header {
	  display: flex;
	  flex-direction: row;
      position: fixed;
      top: 0;
      left: 1%;
      width: 98%;
      justify-content: space-between;
	  align-items: center;
      height: 60px;
      border-bottom-left-radius: 0px; 
	  border-bottom-right-radius: 0px;
	  border-top-left-radius: 8px;
	  border-top-right-radius: 8px;
	  transition: all 0.3s ease;
      user-select: none;


	}



	.nav-links {
		display: flex;
		gap: 20px;
		align-items: center;
		justify-content: center;
	}

	.nav-link {
        display: flex;
        gap: 8px;
        justify-content: center;
        align-items: center;
        background-color: white;
        color: black;
        border-radius: 10px;
        padding: 5px 10px;
        text-decoration: none;
        font-size: 16px;
        transition: all 0.3s ease;
        border: 2px solid transparent;  /* Add this line */
    }

    .nav-link:hover {
        background-color: rgba(0, 0, 0, 0.05);  /* Changed this for better contrast */
        transform: translateY(-2px);
    }

    .nav-link.active {
        background-color: #e6f7ff;  /* Light blue background */
        color: #1890ff;  /* Blue text */
        border-color: #1890ff;  /* Blue border */
        font-weight: bold;
    }

    footer {
	  color: white;
	  text-align: center;
	  justify-content: center;
	  align-items: center;
	  /* padding: 1rem; */
	  width: 100%;
	  position: fixed;
	  bottom: 0;
	  height: 0;
	}

    .overlays-container {
        
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        /* z-index: 1000; */
        transition: right 300ms ease;
    }

    .overlays-container.messages-open {
        right: 300px; /* Width of the messages sidenav */
    }

    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(255, 255, 255, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .content {
        height: 98%;
        width: 98%;
        background-color: #fff;
        /* padding: 20px; */
        border: 1px solid gray;
        border-radius: 8px;
        overflow: auto;
    }

    .messages-sidenav {
        position: fixed;
        top: 60px; /* Adjust based on your new header height */
        right: 0;
        bottom: 0;
        width: 300px;
        background-color: #fff;
        box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
        z-index: 1001;
        overflow-y: auto;
    }

    .close-button {
        position: absolute;
        color: red;
        border-radius: 50%;
        top: 10px;
        right: 10px;
        background-color: transparent;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
    }

    .search-bar {
        flex-grow: 1;
        max-width: 700px;
        margin: 0 20px;
    }

    .search-bar input {
        width: 100%;
        padding: 8px;
        border-radius: 20px;
        border: 1px solid #ccc;
        font-size: 16px;
    }

    .toggle-filter {
        /* position: fixed; */
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        gap: 10px;
        width: 100px;
        border: 1px solid black;
        border-radius: 10px;
        left: 1rem; /* Example of changing the position to the right */
        top: 1rem;
        z-index: 30; /* Ensure it stays on top of the filter overlay and shortcuts */
        background-color: rgb(255, 255, 255); /* Add a background color if necessary to make it stand out */
        padding: 0.5rem; /* Optional padding for better visual clarity */
        cursor: pointer;
    }

    .filter-overlay {
        position: fixed;
        left: 0;
        top: 60px;
        bottom: 0;
        width: 250px;
        background-color: white;
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
        z-index: 20;
    }

    h1 {
        font-size: 30px;
        margin-left: 4rem;
    }

    /* Make sure content areas are properly contained */
    :global(.content-area) {
        max-width: 1400px;  /* Or your preferred max width */
        margin: 0 auto;
        padding: 1rem;
        position: relative;
    }

    /* Add smooth transitions for interactive elements */
    :global(.interactive-element) {
        transition: all 0.2s ease-in-out;
    }

    /* Ensure proper z-indexing */
    :global(.overlay-content) {
        z-index: 1000;
    }

    /* Add responsive container queries */
    @container (min-width: 768px) {
        .main-content {
            padding: 2rem;
        }
    }

    /* Improve focus states for accessibility */
    :global(*:focus-visible) {
        outline: 2px solid #1890ff;
        outline-offset: 2px;
    }


    .main-content {
        margin-top: 60px;  /* Match header height */
        min-height: calc(100vh - 60px);  /* Full viewport height minus header */
        width: 100%;
        background-color: #f5f5f5;  /* Light background for contrast */
        position: relative;
        overflow-x: hidden;
        overflow-y: auto;
        padding: 1rem;
    }

    /* Make sure content areas are properly contained */
    :global(.content-area) {
        max-width: 1400px;  /* Or your preferred max width */
        margin: 0 auto;
        padding: 1rem;
        position: relative;
    }

    /* Add smooth transitions for interactive elements */
    :global(.interactive-element) {
        transition: all 0.2s ease-in-out;
    }

    /* Ensure proper z-indexing */
    :global(.overlay-content) {
        z-index: 1000;
    }

    /* Add responsive container queries */
    @container (min-width: 768px) {
        .main-content {
            padding: 2rem;
        }
    }

    /* Improve focus states for accessibility */
    :global(*:focus-visible) {
        outline: 2px solid #1890ff;
        outline-offset: 2px;
    }
</style>