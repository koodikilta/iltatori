<script lang="ts">
    export let onValueChange: (value: number) => void;
    export let label: string;
    export let currentValue: number = 0;

    let quantity = 1;
    let unitPrice = currentValue || 0;
    
    function calculateTotal() {
        const total = quantity * unitPrice;
        currentValue = total;
        onValueChange(total);
    }

    function handleInput() {
        calculateTotal();
    }

    function clear() {
        quantity = 1;
        unitPrice = 0;
        currentValue = 0;
        onValueChange(0);
    }
</script>

<div class="calculator bg-white shadow rounded-lg p-6">
    <div class="mb-4">
        <span class="text-sm text-gray-600 block mb-2">{label}</span>
        <div class="text-2xl font-bold mb-4">
            {currentValue.toLocaleString('fi-FI', { style: 'currency', currency: 'EUR' })}
        </div>
    </div>
    
    <div class="space-y-4">
        <!-- Quantity Input -->
        <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
                Määrä
            </label>
            <input 
                type="number"
                bind:value={quantity}
                on:input={handleInput}
                min="1"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            />
        </div>

        <!-- Unit Price Input -->
        <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
                Yksikköhinta (€)
            </label>
            <input 
                type="number"
                bind:value={unitPrice}
                on:input={handleInput}
                min="0"
                step="0.01"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
            />
        </div>

        <!-- Action Buttons -->
        <div class="flex space-x-3">
            <button
                on:click={calculateTotal}
                class="flex-1 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
                Päivitä
            </button>
            <button
                on:click={clear}
                class="flex-1 bg-gray-100 text-gray-700 px-4 py-2 rounded hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
                Tyhjennä
            </button>
        </div>
    </div>
</div>

<style>
    /* Add these styles if you want to remove browser's default number input arrows */
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input[type="number"] {
        -moz-appearance: textfield;
    }
</style>