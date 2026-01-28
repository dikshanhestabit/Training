const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const UserSchema = new mongoose.Schema(
  {
    firstName: {
      type: String,
      required: true,
      trim: true,
    },

    lastName: {
      type: String,
      required: true,
      trim: true,
    },

    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      index: true,
    },

    password: {
      type: String,
      required: true,
      minlength: 8,
      select: false, // never return password by default
    },

    status: {
      type: String,
      enum: ['active', 'inactive'],
      default: 'active',
    },
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

/**
 * 🔹 Virtual Field
 * fullName is computed, not stored in DB
 */
UserSchema.virtual('fullName').get(function () {
  return `${this.firstName} ${this.lastName}`;
});

/**
 * 🔹 Pre-save Hook
 * Hash password before saving
 */
UserSchema.pre('save', async function () {
  if (!this.isModified('password')) return next();

  this.password = await bcrypt.hash(this.password, 10);
  
});

/**
 * 🔹 Compound Index
 */
UserSchema.index({ status: 1, createdAt: -1 });

module.exports = mongoose.model('User', UserSchema);
