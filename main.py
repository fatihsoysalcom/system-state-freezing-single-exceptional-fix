import copy

class SystemStateManager:
    """
    Manages the state of a critical system, demonstrating state freezing
    and single exceptional change management during errors.
    """
    def __init__(self, initial_value=1000):
        self._current_value = initial_value
        self._transaction_log = []
        self._is_frozen = False
        self._frozen_snapshot = None # Stores the state at the moment of freezing

    @property
    def current_value(self):
        return self._current_value

    @property
    def transaction_log(self):
        return copy.deepcopy(self._transaction_log) # Return a copy to prevent external modification

    def _log_event(self, event_type, details):
        self._transaction_log.append({"type": event_type, "details": details, "value_after": self._current_value})

    def freeze_state(self, error_details):
        """
        Freezes the system state, preventing further regular operations.
        A snapshot of the state is taken at this moment.
        """
        if not self._is_frozen:
            self._is_frozen = True
            # Store a deep copy of the current state at the point of error
            self._frozen_snapshot = {
                "value": self._current_value,
                "log_length": len(self._transaction_log),
                "error": error_details
            }
            print(f"\n--- SYSTEM FROZEN DUE TO ERROR ---")
            print(f"Error Details: {error_details}")
            print(f"State Snapshot at Freeze: {self._frozen_snapshot}")
            print("Regular operations are now blocked.")
            self._log_event("FREEZE", {"reason": error_details, "snapshot": self._frozen_snapshot})
        else:
            print("System is already frozen.")

    def unfreeze_state(self):
        """
        Unfreezes the system, allowing regular operations to resume.
        """
        if self._is_frozen:
            self._is_frozen = False
            self._frozen_snapshot = None
            print("\n--- SYSTEM UNFROZEN ---")
            self._log_event("UNFREEZE", {})
        else:
            print("System is not frozen.")

    def perform_regular_operation(self, amount, operation_id):
        """
        Simulates a regular operation that modifies the system state.
        This operation is blocked if the system is frozen.
        """
        if self._is_frozen:
            print(f"  [BLOCKED] Operation '{operation_id}' for {amount}. System is frozen.")
            return False

        print(f"\nAttempting regular operation '{operation_id}' (change: {amount})...")
        try:
            # Simulate a multi-step operation
            # Step 1: Pre-check
            if self._current_value + amount < 0 and amount < 0:
                raise ValueError("Insufficient funds for this deduction.")

            # Step 2: Simulate a critical error during processing
            if operation_id == "OP_CRITICAL_FAIL" and amount == -200:
                print(f"  Simulating critical system failure during '{operation_id}'...")
                raise RuntimeError("Critical internal service dependency failed.")

            # Step 3: Apply change
            self._current_value += amount
            self._log_event("OPERATION", {"id": operation_id, "amount": amount, "status": "completed"})
            print(f"  Operation '{operation_id}' completed. Current value: {self._current_value}")
            return True

        except Exception as e:
            print(f"  Operation '{operation_id}' FAILED: {e}")
            # --- Concept: Freezing State ---
            # When a critical error occurs, freeze the system state.
            # This prevents further uncontrolled modifications.
            self.freeze_state(f"Operation '{operation_id}' failed: {e}")
            return False

    def apply_exceptional_fix(self, fix_type, fix_parameters):
        """
        Applies a single, exceptional change to rectify an issue while the system is frozen.
        This bypasses the normal operation blocking. After the fix, the system is typically unfrozen.
        """
        print(f"\n--- Applying EXCEPTIONAL FIX: '{fix_type}' ---")
        if fix_type == "adjust_value":
            adjustment_amount = fix_parameters.get("amount", 0)
            reason = fix_parameters.get("reason", "Unspecified exceptional adjustment")

            # --- Concept: Single Exceptional Change ---
            # This is the ONLY allowed modification while frozen,
            # designed to specifically address the root cause.
            self._current_value += adjustment_amount
            self._log_event("EXCEPTIONAL_FIX", {"type": fix_type, "amount": adjustment_amount, "reason": reason})
            print(f"  Value adjusted by {adjustment_amount}. New value: {self._current_value}")
            print("  Exceptional fix applied successfully.")
            self.unfreeze_state() # Unfreeze after the fix
            return True
        else:
            print(f"  Unknown exceptional fix type: '{fix_type}'.")
            return False

# --- DEMONSTRATION ---
if __name__ == "__main__":
    system = SystemStateManager(initial_value=1000)
    print(f"Initial System Value: {system.current_value}")

    # 1. Perform some regular operations
    system.perform_regular_operation(100, "OP_DEPOSIT_1")
    system.perform_regular_operation(-50, "OP_WITHDRAW_1")

    # 2. Simulate a critical error that causes the system to freeze
    system.perform_regular_operation(-200, "OP_CRITICAL_FAIL")

    # 3. Attempt another regular operation while the system is frozen
    # This operation should be blocked, demonstrating the "frozen state" principle.
    system.perform_regular_operation(75, "OP_BLOCKED_DEPOSIT")

    # 4. Apply a single, exceptional fix to resolve the issue
    # Here, we assume the 'OP_CRITICAL_FAIL' intended to deduct 200, but failed mid-way,
    # leaving the system in an inconsistent state. We apply a fix to correct the balance.
    # For example, if the deduction never actually happened due to the error, we might need to add it back.
    system.apply_exceptional_fix(
        "adjust_value",
        {"amount": 200, "reason": "Reversing partial effect of failed OP_CRITICAL_FAIL"}
    )

    # 5. After the fix and unfreeze, regular operations can resume
    system.perform_regular_operation(150, "OP_RESUME_DEPOSIT")

    print(f"\n--- FINAL SYSTEM STATE ---")
    print(f"Final System Value: {system.current_value}")
    print(f"Full Transaction Log:")
    for entry in system.transaction_log:
        print(f"  - {entry}")
