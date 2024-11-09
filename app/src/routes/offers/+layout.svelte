<script lang="ts">
    import type { OfferData, CostSectionKey } from '$lib/types/typeOffer';
    import { offerStore, offerTotals } from '$lib/stores/offerStore';
    import { onMount } from 'svelte';
    onMount(() => {
        console.log('the component has mounted');
    });
    // Subscribe to store at layout level
    $: offer = $offerStore;
    $: totals = $offerTotals;
</script>

<div class="max-w-7xl mx-auto p-4">
    <slot />
</div>

<style>
    .offers-layout {
        @apply max-w-7xl mx-auto p-4;
    }
</style>