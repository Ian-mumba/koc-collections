(() => {
  const storageKey = 'koc_inventory';
  const defaultInventory = [
    { id: 1, name: 'Classic Fashion Item', price: 450, originalPrice: 600, images: ['five 5.jpg'], category: 'accessories' },
    { id: 2, name: 'Premium Outfit', price: 300, images: ['four 4.jpg'], category: 'women' },
    { id: 3, name: 'Smart Attire', price: 1500, images: ['six 6.jpg'], category: 'men' },
    { id: 4, name: 'Premium Suit', price: 1200, originalPrice: 2800, images: ['two 2.jpg'], category: 'men' },
    { id: 5, name: 'Signature Street Look', price: 900, originalPrice: 1400, images: ['three 3.jpg'], category: 'women' }
  ];

  function isValidProduct(product) {
    return product &&
      Number.isFinite(Number(product.id)) &&
      typeof product.name === 'string' &&
      Number.isFinite(Number(product.price)) &&
      ['men', 'women', 'accessories'].includes(product.category) &&
      Array.isArray(product.images) &&
      product.images.length > 0 &&
      product.images.every(image => typeof image === 'string' && image.length > 0);
  }

  window.loadKocInventory = function() {
    let savedInventory = [];
    try {
      const storedValue = localStorage.getItem(storageKey);
      const parsedInventory = storedValue ? JSON.parse(storedValue) : [];
      if (Array.isArray(parsedInventory)) {
        savedInventory = parsedInventory.filter(isValidProduct);
      }
    } catch {
      savedInventory = [];
    }

    const inventoryById = new Map();
    for (const product of defaultInventory) inventoryById.set(product.id, product);
    for (const product of savedInventory) inventoryById.set(Number(product.id), product);
    const inventory = [...inventoryById.values()];

    try {
      localStorage.setItem(storageKey, JSON.stringify(inventory));
    } catch {
      // Keep the in-memory inventory usable when storage is unavailable or full.
    }
    return inventory;
  };

  window.escapeKocHtml = function(value) {
    return String(value).replace(/[&<>"']/g, character => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[character]);
  };
})();