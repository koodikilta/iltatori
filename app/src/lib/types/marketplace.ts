export interface MarketplaceItem {
    name: string;
    price: number;
    image: string;
    // Add more properties as needed
    description?: string;
    category?: string;
    tags?: string[];
    seller?: {
        id: string;
        name: string;
        rating: number;
    };
}

export interface FilterState {
    category?: string;
    minPrice?: number;
    maxPrice?: number;
    sortBy?: 'price' | 'name' | 'date' | 'rating';
    sortOrder?: 'asc' | 'desc';
}

export interface CategoryItem {
    id: string;
    name: string;
    icon?: string;
    subCategories?: CategoryItem[];
}