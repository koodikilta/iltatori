<script lang="ts">
    import type { LabelCardProps } from '$lib/types/typeOffer';

    export let title: string;
    export let labels: LabelCardProps['labels'];
    export let summary: LabelCardProps['summary'];
    export let total: number;
    export let onFieldSelect: (field: string) => void;
    export let activeField: string | null = null;

    function handleFieldClick(fieldId: string) {
        onFieldSelect(fieldId);
    }
</script>

<section class="card card-hover">
    <h2 class="card-title">{title}</h2>
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <!-- Input Fields Column -->
        <div class="space-y-4 relative z-20">
            {#each labels as item}
                <label 
                    class="block relative field-hover p-3"
                    class:field-active={activeField === item.id}
                    on:click={() => handleFieldClick(item.id)}
                >
                    <span class="text-gray-700 block mb-1 font-medium">
                        {item.label}
                    </span>
                    <input
                        type="number"
                        value={item.value}
                        on:input={(e) => item.bind(parseFloat(e.currentTarget.value) || 0)}
                        class="input-hover mt-1 block w-full rounded-md border-gray-300 
                               shadow-sm focus:border-blue-500 focus:ring-blue-500 
                               {activeField === item.id ? 'border-blue-500' : ''}"
                        placeholder="0.00"
                        step="0.01"
                        min="0"
                    />
                </label>
            {/each}
        </div>

        <!-- Summary Column -->
        <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="font-medium text-gray-900 mb-4">
                Yhteenveto {title.toLowerCase()}sta
            </h3>
            <div class="space-y-1">
                {#each summary as item}
                    <div 
                        class="summary-row-hover flex justify-between items-center"
                        class:field-active={activeField === item.label}
                    >
                        <span class="text-gray-600">{item.label}</span>
                        <span class="font-medium">€{item.value.toFixed(2)}</span>
                    </div>
                {/each}
                <div class="pt-3 mt-3 border-t border-gray-200">
                    <div class="summary-row-hover flex justify-between items-center font-semibold">
                        <span>Yhteensä</span>
                        <span>€{total.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<style>
    input[type="number"]::-webkit-inner-spin-button,
    input[type="number"]::-webkit-outer-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    input[type="number"] {
        -moz-appearance: textfield;
    }

    /* Optional: Add smooth transitions for active state */
    .field-active {
        transition: all 0.2s ease-in-out;
    }
</style>