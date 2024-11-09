<script lang="ts">
    import type { PaymentTerms } from '$lib/types/typeOffer';

    export let paymentTerms: PaymentTerms;
    export let onUpdate: (field: keyof PaymentTerms, value: boolean | number) => void;
</script>

<section class="card">
    <h2 class="card-title">Maksuehdot</h2>
    <div class="space-y-4">
        <label class="flex items-center space-x-2">
            <input 
                type="checkbox"
                checked={paymentTerms.requiresAdvancePayment}
                on:change={(e) => onUpdate('requiresAdvancePayment', e.currentTarget.checked)}
                class="form-checkbox"
            />
            <span class="text-label">Ennakkomaksu vaaditaan</span>
        </label>

        <label class="flex items-center space-x-2">
            <input 
                type="checkbox"
                checked={paymentTerms.singleInvoice}
                on:change={(e) => onUpdate('singleInvoice', e.currentTarget.checked)}
                class="form-checkbox"
            />
            <span class="text-label">Yksi lasku</span>
        </label>

        <div class="form-group">
            <label class="form-label">Osamaksun kynnysarvo</label>
            <input 
                type="number"
                value={paymentTerms.partialPaymentThreshold}
                on:input={(e) => onUpdate('partialPaymentThreshold', parseFloat(e.currentTarget.value))}
                class="form-input"
            />
        </div>

        <div class="form-group">
            <label class="form-label">Osamaksun prosentti</label>
            <input 
                type="number"
                value={paymentTerms.partialPaymentPercentage}
                on:input={(e) => onUpdate('partialPaymentPercentage', parseFloat(e.currentTarget.value))}
                class="form-input"
            />
        </div>
    </div>
</section>