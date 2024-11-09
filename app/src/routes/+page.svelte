<script lang="ts">
    import "../app.css";
    import { fly } from 'svelte/transition';
    import type { MarketplaceItem } from '$lib/types/marketplace';  // Create this type
    import CategorySelector from '$lib/components/ui/CategorySelector.svelte';
    import FilterSelector from '$lib/components/ui/FilterSelector.svelte';
    import SortSelector from '$lib/components/ui/SortSelector.svelte';
    import ItemCard from '$lib/components/ui/ItemCard.svelte';
    import { Filter, FilterX } from 'lucide-svelte';

    let showFilterSelector = false;

    const items: MarketplaceItem[] = [
      { name: 'Apple', price: 0.5, image: 'https://example.com/apple.jpg' },
      { name: 'Banana', price: 0.3, image: 'https://example.com/banana.jpg' },
      { name: 'Orange', price: 0.6, image: 'https://example.com/orange.jpg' },
      { name: 'Mango', price: 1.2, image: 'https://example.com/mango.jpg' },
      { name: 'Apple', price: 0.5, image: 'https://example.com/apple.jpg' },
      { name: 'Banana', price: 0.3, image: 'https://example.com/banana.jpg' },
      { name: 'Orange', price: 0.6, image: 'https://example.com/orange.jpg' },
      { name: 'Mango', price: 1.2, image: 'https://example.com/mango.jpg' },
      { name: 'Apple', price: 0.5, image: 'https://example.com/apple.jpg' },
      { name: 'Banana', price: 0.3, image: 'https://example.com/banana.jpg' },
      { name: 'Orange', price: 0.6, image: 'https://example.com/orange.jpg' },
      { name: 'Mango', price: 1.2, image: 'https://example.com/mango.jpg' },
    ];
</script>

<div class="page-container">
    
    <div class="filter-shortcuts" transition:fly={{ x: -40, duration: 300 }}>
        
    </div>

    <div class="main-content">
        <CategorySelector />
        <SortSelector />
        <div class="item-grid">
            {#each items as item}
                <ItemCard {...item} />
            {/each}
        </div>
    </div>
</div>

<style>
    .page-container {
        position: relative;
    }

    .filter-shortcuts {
        position: fixed;
        left: 0;
        top: 60px;
        bottom: 0;
        width: 40px;
        background-color: white;
        border-right: 1px solid rgb(220, 220, 220);
        /* box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1); */
        z-index: 20;
    }

    .toggle-filter {
        position: fixed;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        gap: 10px;
        border: 1px solid black;
        border-radius: 10px;
        left: 1rem; /* Example of changing the position to the right */
        top: 1rem;
        z-index: 30; /* Ensure it stays on top of the filter overlay and shortcuts */
        background-color: rgb(101, 101, 101); /* Add a background color if necessary to make it stand out */
        padding: 0.5rem; /* Optional padding for better visual clarity */
        cursor: pointer;
    }

    .main-content {
        padding: 1rem;
        padding-left: 3rem; /* Add some padding to account for the toggle button */
        width: 100%;
        box-sizing: border-box;
        overflow-x: hidden;
    }

    .item-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }

    /* Ensure CategorySelector and ItemCard components fill the width */
    :global(.main-content > :global(div)) {
        width: 100%;
    }
</style>