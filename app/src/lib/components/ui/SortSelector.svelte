<!-- lib/components/ui/SortSelector.svelte -->
<script lang="ts">
    let sortOption = 'price-asc';
  
    function handleSort(event: Event) {
      sortOption = (event.target as HTMLSelectElement).value;
      // Implement sorting logic here
    }
  </script>
  
  <div class="sort-selector">
    <select bind:value={sortOption} on:change={handleSort}>
      <option value="price-asc">Price: Low to High</option>
      <option value="price-desc">Price: High to Low</option>
      <option value="name-asc">Name: A to Z</option>
      <option value="name-desc">Name: Z to A</option>
    </select>
  </div>
  
  <style>
    .sort-selector {
      margin-bottom: 1rem;
      padding: 1rem;

    }
  
    select {
      padding: 0.5rem;
      border-radius: 4px;
      border: 1px solid #ccc;
    }
  </style>