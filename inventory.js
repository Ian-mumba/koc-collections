(() => {
  function isValidProduct(product) {
    return product &&
      typeof product.name === 'string' &&
      Number.isFinite(Number(product.price)) &&
      ['men', 'women', 'accessories'].includes(product.category) &&
      Array.isArray(product.images) &&
      product.images.length > 0 &&
      product.images.every(image => typeof image === 'string' && image.length > 0);
  }

  window.loadKocInventory = async function() {
    const response = await fetch('products.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Product catalog could not be loaded.');

    const inventory = await response.json();
    if (!Array.isArray(inventory)) throw new Error('Product catalog has an invalid format.');
    return inventory.filter(isValidProduct);
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