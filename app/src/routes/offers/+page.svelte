<script lang="ts">
    import type { OfferData, CostSectionKey, PaymentTerms } from '$lib/types/typeOffer';
    import { offerStore } from '$lib/stores/offerStore';
    import CostsSection from '../../lib/components/ui/CostsSection.svelte';
    import PaymentSection from '../../lib/components/ui/PaymentSection.svelte';
    import "/src/app.css";
    import { onMount } from 'svelte';

    let project = $offerStore;

    // Handler function for cost updates
    function handleCostsUpdate(section: CostSectionKey, field: string, value: number) {
        offerStore.updateCost(section, field, value);
    }

    // Handler function for payment updates
    function handlePaymentUpdate(field: keyof PaymentTerms, value: boolean | number) {
        const updatedPaymentTerms = { ...project.paymentTerms, [field]: value };
        project = { ...project, paymentTerms: updatedPaymentTerms };
        offerStore.set(project);
    }

    onMount(() => {
        console.log('the component has mounted');
    });

    // Subscribe to store changes
    $: project = $offerStore;
</script>

<div class="grid-main container-padding">
    <div class="section-spacing">
        <CostsSection 
            costs={project}
            onUpdate={handleCostsUpdate}
        />

        <!-- Total Summary Section -->
        <section class="card">
            <h2 class="card-title">Yhteenveto</h2>
            <div class="section-spacing">
                <div class="summary-row">
                    <span class="summary-label">Työt yhteensä</span>
                    <span class="summary-value">
                        €{project.workCosts.total.toFixed(2)}
                    </span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Tarvikkeet yhteensä</span>
                    <span class="summary-value">
                        €{project.materialCosts.total.toFixed(2)}
                    </span>
                </div>
                <div class="summary-row text-red-600">
                    <span class="summary-label">Alennukset yhteensä</span>
                    <span class="summary-value">
                        -€{project.materialCosts.discount.toFixed(2)}
                    </span>
                </div>
                <div class="summary-divider">
                    <div class="flex-between">
                        <span>Kokonaishinta (ALV {project.pricing.vatPercentage}%)</span>
                        <span class="text-total">
                            €{project.pricing.totalPriceWithVat.toFixed(2)}
                        </span>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <div class="sticky-container">
        <PaymentSection 
            paymentTerms={project.paymentTerms}
            onUpdate={handlePaymentUpdate}
        />

        <!-- Tax Deduction Info -->
        <section class="card">
            <h2 class="card-subtitle">Kotitalousvähennys</h2>
            <div class="space-y-2 text-label">
                <p>Vähennyksen määrä on {project.taxDeduction.deductionPercentage}% työstä</p>
                <p>Henkilökohtainen maksimi: €{project.taxDeduction.maxDeductionPerPerson}</p>
                <p>Omavastuu: €{project.taxDeduction.personalLiability}</p>
                <div class="summary-divider">
                    <div class="flex-between">
                        <span>Arvioitu vähennys:</span>
                        <span class="summary-value">
                            €{project.taxDeduction.personalDeduction.toFixed(2)}
                        </span>
                    </div>
                </div>
            </div>
        </section>
    </div>
</div>