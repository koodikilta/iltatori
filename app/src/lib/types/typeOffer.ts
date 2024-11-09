export type CostSectionKey = 'workCosts' | 'materialCosts' | 'additionalCosts';

export interface WorkCosts {
    total: number;
    construction: number;
    plumbing: number;
    electrical: number;
    glazing: number;
    [key: string]: number;
}

export interface MaterialCosts {
    total: number;
    construction: number;
    hvacMaterials: number;
    glazingMaterials: number;
    surfaceMaterialsAndFixtures: number;
    discount: number;
    [key: string]: number;
}

export interface AdditionalCosts {
    total: number;
    wasteAndFreight: number;
    additionalServices: number;
    [key: string]: number;
}

export interface Campaign {
    description: string;
    discount: number;
    
}

export interface TaxDeduction {
    personalDeduction: number;
    coupleDeduction: number;
    deductionPercentage: number;
    maxDeductionPerPerson: number;
    personalLiability: number;
}

export interface PricingDetails {
    totalPriceWithVat: number;
    vatPercentage: number;
    priceAfterPersonalDeduction: number;
    priceAfterCoupleDeduction: number;
}

export interface PaymentTerms {
    requiresAdvancePayment: boolean;
    singleInvoice: boolean;
    partialPaymentThreshold: number;
    partialPaymentPercentage: number;
    customBenchworkInvoicing: boolean;
    financingAvailable: boolean;
}

export interface Warranty {
    constructionWarrantyMonths: number;
    termsReference: string;
    materialsWarrantyType: string;
}

export interface OfferData {
    workCosts: WorkCosts;
    materialCosts: MaterialCosts;
    additionalCosts: AdditionalCosts;
    campaign: Campaign;
    taxDeduction: TaxDeduction;
    pricing: PricingDetails;
    paymentTerms: PaymentTerms;
    warranty: Warranty;
}

// Helper type for the update function
export type UpdateFunction = (section: CostSectionKey, field: string, value: number) => void;



export interface LabelCardProps {
    title: string;
    labels: LabelItem[];
    summary: { label: string; value: number; }[];
    total: number;
    onFieldSelect: (field: string) => void;  // Changed to only accept string
    activeField: string | null;
}

export interface LabelItem {
    id: string;
    label: string;
    value: number;
    bind: (value: number) => void;
}

export interface CostsSectionProps {
    costs: {
        workCosts: WorkCosts;
        materialCosts: MaterialCosts;
        additionalCosts: AdditionalCosts;
    };
    onUpdate: (section: CostSectionKey, field: string, value: number) => void;
}

export type FieldSelectHandler = (section: CostSectionKey, field: string) => void;