<!-- lib/components/ui/ItemCard.svelte -->
<script lang="ts">
    export let name: string;
    export let price: number;
    export let image: string;
  </script>
  
  <div class="item-card">
    <img src={image} alt={name} />
    <h3>{name}</h3>
    <p>${price.toFixed(2)}</p>
    <button>Add to Cart</button>
  </div>
  
  <style>
    .item-card {
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
  
    img {
      width: 100%;
      height: 200px;
      object-fit: cover;
      border-radius: 4px;
      margin-bottom: 1rem;
    }
  
    button {
      margin-top: 1rem;
      padding: 0.5rem 1rem;
      background-color: #4CAF50;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  
    button:hover {
      background-color: #45a049;
    }
  </style>