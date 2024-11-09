// src/lib/utils/calculations.ts
import type { OfferData } from '$lib/types/typeOffer';

export const calculateTotals = (offer: OfferData): OfferData => {
    const workTotal = 
        offer.workCosts.construction +
        offer.workCosts.plumbing +
        offer.workCosts.electrical +
        offer.workCosts.glazing;

    const materialsTotal = 
        offer.materialCosts.construction +
        offer.materialCosts.hvacMaterials +
        offer.materialCosts.glazingMaterials +
        offer.materialCosts.surfaceMaterialsAndFixtures -
        offer.materialCosts.discount;

    const additionalTotal = 
        offer.additionalCosts.wasteAndFreight +
        offer.additionalCosts.additionalServices;

    const subtotal = workTotal + materialsTotal + additionalTotal - offer.campaign.discount;
    const totalWithVat = subtotal * (1 + offer.pricing.vatPercentage / 100);

    return {
        ...offer,
        workCosts: {
            ...offer.workCosts,
            total: workTotal
        },
        materialCosts: {
            ...offer.materialCosts,
            total: materialsTotal
        },
        additionalCosts: {
            ...offer.additionalCosts,
            total: additionalTotal
        },
        pricing: {
            ...offer.pricing,
            totalPriceWithVat: totalWithVat,
            priceAfterPersonalDeduction: totalWithVat - offer.taxDeduction.personalDeduction,
            priceAfterCoupleDeduction: totalWithVat - offer.taxDeduction.coupleDeduction
        }
    };
};