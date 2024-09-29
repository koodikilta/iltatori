<!-- lib/components/ui/CategorySelector.svelte -->
<script lang="ts">
    import { fly } from 'svelte/transition';
  
    interface Category {
      icon: string;
      text: string;
      description: string;
    }
  
    const categories: Category[] = [
      { icon: '🍎', text: 'Fruits', description: 'Fresh and juicy fruits' },
      { icon: '🥕', text: 'Vegetables', description: 'Crisp and healthy vegetables' },
      { icon: '🍖', text: 'Meat', description: 'Quality cuts of meat' },
      { icon: '🥛', text: 'Dairy', description: 'Fresh dairy products' },
      { icon: '🍞', text: 'Bakery', description: 'Freshly baked goods' },
      { icon: '🐟', text: 'Seafood', description: 'Fresh seafood options' },
      { icon: '🥫', text: 'Canned Goods', description: 'Long-lasting canned products' },
      { icon: '🧊', text: 'Frozen Foods', description: 'Convenient frozen meals and ingredients' },
    ];
  </script>
  
  <div class="category-grid">
    {#each categories as category}
      <button class="category-button" on:click>
        <span class="icon-text">
          <span class="icon">{category.icon}</span>
          <span class="text">{category.text}</span>
        </span>
        <span class="description">{category.description}</span>
      </button>
    {/each}
  </div>
  
  <style>
    .category-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      padding: 1rem;
      width: 90vh;

    }
  
    .category-button {
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      border: 1px solid #ccc;
      border-radius: 8px;
      background-color: white;
      cursor: pointer;
      overflow: hidden;
      transition: all 0.3s ease;
    }
  
    .icon-text {
      display: flex;
      flex-direction: column;
      align-items: center;
      transition: opacity 0.3s ease;
    }
  
    .icon {
      font-size: 2rem;
      margin-bottom: 0.5rem;
    }
  
    .text {
      font-size: 1rem;
    }
  
    .description {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0.5rem;
      background-color: rgba(255, 255, 255, 0.9);
      opacity: 0;
      transition: opacity 0.3s ease;
    }
  
    .category-button:hover .icon-text {
      opacity: 0;
    }
  
    .category-button:hover .description {
      opacity: 1;
    }
  </style>