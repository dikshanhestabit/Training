const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },

    price: {
      type: Number,
      required: true,
      min: 0,
    },

    rating: {
      type: Number,
      default: 0,
      min: 0,
      max: 5,
    },

    status: {
      type: String,
      enum: ['active', 'inactive'],
      default: 'active',
    },

    tags: {
      type: [String],
      default: [],
      index: true,
    },

    deletedAt: {
      type: Date,
      default: null,
      index: true,
    },
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
  }
);

/**Virtual Field */
ProductSchema.virtual('ratingLabel').get(function () {
  if (this.rating >= 4) return 'Excellent';
  if (this.rating >= 2) return 'Average';
  return 'Poor';
});

/** Compound Index */
ProductSchema.index({ status: 1, createdAt: -1 });

module.exports = mongoose.model('Product', ProductSchema);
