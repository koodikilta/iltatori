import { writable, derived } from 'svelte/store';
import type { OfferData, CostSectionKey } from '$lib/types/typeOffer';

function createOfferStore() {

    const initialState: OfferData = {
        workCosts: {
            total: 0,
            construction: 0,
            plumbing: 0,
            electrical: 0,
            glazing: 0
        },
        materialCosts: {
            total: 0,
            construction: 0,
            hvacMaterials: 0,
            glazingMaterials: 0,
            surfaceMaterialsAndFixtures: 0,
            discount: 0
        },
        additionalCosts: {
            total: 0,
            wasteAndFreight: 0,
            additionalServices: 0
        },
        campaign: {
            description: 'Floor heating included',
            discount: 520
        },
        taxDeduction: {
            personalDeduction: 2250,
            coupleDeduction: 4500,
            deductionPercentage: 40,
            maxDeductionPerPerson: 2250,
            personalLiability: 100
        },
        pricing: {
            totalPriceWithVat: 0,
            vatPercentage: 25.5,
            priceAfterPersonalDeduction: 0,
            priceAfterCoupleDeduction: 0
        },
        paymentTerms: {
            requiresAdvancePayment: false,
            singleInvoice: true,
            partialPaymentThreshold: 40000,
            partialPaymentPercentage: 50,
            customBenchworkInvoicing: true,
            financingAvailable: true
        },
        warranty: {
            constructionWarrantyMonths: 24,
            termsReference: 'YSE 1998',
            materialsWarrantyType: 'Manufacturer warranty'
        }
    };

    const { subscribe, set, update } = writable<OfferData>(initialState);

    function calculateTotals(data: OfferData): OfferData {
        const workTotal = Object.values(data.workCosts).reduce((sum, value) => sum + value, 0);
        const materialTotal = Object.values(data.materialCosts).reduce((sum, value) => sum + value, 0);
        const additionalTotal = Object.values(data.additionalCosts).reduce((sum, value) => sum + value, 0);
        
        const subtotal = workTotal + materialTotal - data.materialCosts.discount + additionalTotal;
        const vatAmount = subtotal * (data.pricing.vatPercentage / 100);

        const workDeduction = Math.min(
            (workTotal * data.taxDeduction.deductionPercentage) / 100,
            data.taxDeduction.maxDeductionPerPerson
        );

        const updatedData = {
            ...data,
            workCosts: { ...data.workCosts, total: workTotal },
            materialCosts: { ...data.materialCosts, total: materialTotal },
            additionalCosts: { ...data.additionalCosts, total: additionalTotal },
            pricing: {
                ...data.pricing,
                totalPriceWithVat: subtotal + vatAmount,
                priceAfterPersonalDeduction: subtotal + vatAmount - workDeduction,
                priceAfterCoupleDeduction: subtotal + vatAmount - (workDeduction * 2)
            },
            taxDeduction: { ...data.taxDeduction, personalDeduction: workDeduction, coupleDeduction: workDeduction * 2 }
        };
        
        return updatedData;
    }

    return {
        subscribe,
        set,
        updateCost: (section: CostSectionKey, field: string, value: number) => {
            update(currentData => {
                const updatedValue = { ...currentData[section], [field]: value };
                const updatedSection = { ...currentData, [section]: updatedValue };
                const updatedData = calculateTotals(updatedSection);
                return updatedData;
            });
        },
        reset: () => set(initialState)
    };
}

export const offerStore = createOfferStore();

// Derived store for totals
export const offerTotals = derived(offerStore, $offer => ({
    workTotal: $offer.workCosts.total,
    materialTotal: $offer.materialCosts.total,
    additionalTotal: $offer.additionalCosts.total,
    totalWithVat: $offer.pricing.totalPriceWithVat,
    discount: $offer.materialCosts.discount,
    vatAmount: $offer.pricing.totalPriceWithVat - 
        ($offer.workCosts.total + $offer.materialCosts.total - $offer.materialCosts.discount + $offer.additionalCosts.total)
}));