<script lang="ts">
    import { onMount } from 'svelte';

    import type { WorkCosts, MaterialCosts, AdditionalCosts, CostSectionKey, LabelItem } from '$lib/types/typeOffer';
    import "/src/app.css";

    export let costs: {
        workCosts: WorkCosts;
        materialCosts: MaterialCosts;
        additionalCosts: AdditionalCosts;
    };
    export let onUpdate: (section: CostSectionKey, field: string, value: number) => void;

    onMount(() => {
        console.log('the component has mounted');
    });

    let activeSection: CostSectionKey | null = null;
    let activeFieldId: string | null = null;

    function handleFieldSelect(section: CostSectionKey, fieldId: string) {
        activeSection = section;
        activeFieldId = fieldId;
    }

    function getLabelForKey(key: string): string {
        const labels: Record<string, string> = {
            construction: 'Rakennustyöt',
            plumbing: 'Putkityöt',
            electrical: 'Sähkötyöt',
            glazing: 'Lasitustyöt',
            hvacMaterials: 'LVIS-tarvikkeet',
            glazingMaterials: 'Lasitustarvikkeet',
            surfaceMaterialsAndFixtures: 'Pintamateriaalit ja kalusteet',
            discount: 'Alennus',
            wasteAndFreight: 'Jäte- ja rahtikustannukset',
            additionalServices: 'Lisäpalvelut'
        };
        return labels[key] || key;
    }

    function createLabels(section: CostSectionKey, items: Record<string, number>, skipFields: string[] = ['total']): LabelItem[] {
        return Object.entries(items)
            .filter(([key]) => !skipFields.includes(key))
            .map(([key, value]) => ({
                id: key,
                label: getLabelForKey(key),
                value,
                bind: (newValue: number) => onUpdate(section, key, newValue)
            }));
    }

    let workLabels: LabelItem[] = [];
    let materialLabels: LabelItem[] = [];
    let additionalLabels: LabelItem[] = [];

    $: {
        workLabels = createLabels('workCosts', costs.workCosts);
        materialLabels = createLabels('materialCosts', costs.materialCosts);
        additionalLabels = createLabels('additionalCosts', costs.additionalCosts);
        console.log('workLabels:', workLabels);
        console.log('materialLabels:', materialLabels);
        console.log('additionalLabels:', additionalLabels);
    }

    let workSummary = workLabels.map(({ label, value }) => ({ label, value }));
    let materialSummary = materialLabels.map(({ label, value }) => ({ label, value }));
    let additionalSummary = additionalLabels.map(({ label, value }) => ({ label, value }));

    console.log('workSummary:', workSummary);
    console.log('materialSummary:', materialSummary);
    console.log('additionalSummary:', additionalSummary);
</script>

<div class="costs-container space-y-8">
    <!-- Työkustannukset-osio -->
    <section class="card">
        <h2 class="section-title">Työt</h2>
        <div class="grid-layout">
            <div class="field-group">
                {#each workLabels as item}
                    <div
                        class="interactive-field"
                        class:active={activeSection === 'workCosts' && activeFieldId === item.id}
                        on:click={() => handleFieldSelect('workCosts', item.id)}>
                        <span class="field-label">{item.label}</span>
                        <span
                            contenteditable="true"
                            on:input={e => item.bind(parseFloat(e.currentTarget.innerText) || 0)}
                            class="form-input"
                            placeholder="0.00">
                            {item.value}
                        </span>
                    </div>
                {/each}
            </div>

            <div class="summary-section">
                <h3 class="font-medium text-gray-900 mb-4">Yhteenveto töistä</h3>
                {#each workSummary as item}
                    <div class="summary-row">
                        <span class="text-gray-600">{item.label}</span>
                        <span class="font-medium">€{item.value.toFixed(2)}</span>
                    </div>
                {/each}
                <div class="pt-3 mt-3 border-t border-gray-200">
                    <div class="summary-row font-semibold">
                        <span>Yhteensä</span>
                        <span>€{costs.workCosts.total.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Tarvikekustannukset-osio -->
    <section class="card">
        <h2 class="section-title">Tarvikkeet</h2>
        <!-- Samankaltainen rakenne kuin työkustannuksissa... -->
    </section>

    <!-- Lisäkustannukset-osio -->
    <section class="card">
        <h2 class="section-title">Lisäkustannukset</h2>
        <!-- Samankaltainen rakenne kuin työkustannuksissa... -->
    </section>
</div>

<style>
    :global(.costs-container) {
        @apply relative;
        transition: all 0.3s ease;
        padding: 10px;
    }

    :global(input[type="number"]::-webkit-inner-spin-button),
    :global(input[type="number"]::-webkit-outer-spin-button) {
        -webkit-appearance: none;
        margin: 0;
    }

    :global(input[type="number"]) {
        -moz-appearance: textfield;
    }
</style>