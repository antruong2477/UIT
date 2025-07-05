import numpy as np
import matplotlib.pyplot as plt

# --- Phần 1: Chuyển đổi Tín hiệu Analog sang Chuỗi Xung (Biến thể Mã hóa Tốc độ) ---
def convert_analog_value_to_poisson_spikes(
    signal_level,
    observation_duration_s,
    simulation_dt_s,
    max_firing_rate_hz
):
    """
    Chuyển đổi một mức tín hiệu analog không đổi thành một chuỗi xung kiểu Poisson.
    Giả định signal_level không đổi trong suốt cửa sổ quan sát.

    Args:
        signal_level (float): Mức tín hiệu đầu vào (ví dụ: cường độ pixel).
                              Giả định đã được chuẩn hóa trong khoảng [0, 1].
        observation_duration_s (float): Tổng thời gian để tạo chuỗi xung (giây).
        simulation_dt_s (float): Bước thời gian cho mô phỏng (giây).
        max_firing_rate_hz (float): Tần số xung tối đa (Hz) ứng với signal_level là 1.

    Returns:
        tuple: (spike_train_binary, time_points_s)
               spike_train_binary (np.array): Mảng 1D, 1 nếu có xung, 0 nếu không.
               time_points_s (np.array): Các điểm thời gian tương ứng.
    """
    if not (0 <= signal_level <= 1):
        original_signal_level = signal_level
        signal_level = np.clip(signal_level, 0, 1)
        # print(f"Cảnh báo: Mức tín hiệu {original_signal_level} đã được giới hạn về {signal_level}")

    num_steps = int(observation_duration_s / simulation_dt_s)
    time_points_s = np.linspace(0, observation_duration_s, num_steps, endpoint=False)
    spike_train_binary = np.zeros(num_steps, dtype=int)

    # Tính toán tốc độ dựa trên mức tín hiệu
    expected_rate_hz = signal_level * max_firing_rate_hz

    for i in range(num_steps):
        # Xác suất có một xung trong bước thời gian nhỏ này
        spike_probability = expected_rate_hz * simulation_dt_s
        if np.random.rand() < spike_probability:
            spike_train_binary[i] = 1

    return spike_train_binary, time_points_s


def convert_timeseries_to_poisson_spikes(
    analog_signal_data,
    total_duration_s,
    time_step_s,
    peak_frequency_hz
):
    """
    Chuyển đổi một tín hiệu analog biến thiên theo thời gian thành một chuỗi xung Poisson
    sử dụng mã hóa tốc độ (rate coding).

    Args:
        analog_signal_data (np.array): Tín hiệu đầu vào liên tục 1D.
        total_duration_s (float): Tổng thời gian cho chuỗi xung (giây).
        time_step_s (float): Bước thời gian mô phỏng (giây).
        peak_frequency_hz (float): Tần số xung tối đa (Hz) ứng với giá trị lớn nhất của tín hiệu.

    Returns:
        tuple: (output_spike_train, simulation_time_axis, resampled_signal)
               output_spike_train (np.array): Mảng 1D, 1 nếu có xung, 0 nếu không.
               simulation_time_axis (np.array): Các điểm thời gian tương ứng.
               resampled_signal (np.array): Tín hiệu được nội suy để khớp với simulation_time_axis.
    """
    num_simulation_steps = int(total_duration_s / time_step_s)
    simulation_time_axis = np.linspace(0, total_duration_s, num_simulation_steps, endpoint=False)

    # Đảm bảo độ dài tín hiệu khớp với num_simulation_steps, nội suy nếu cần
    if len(analog_signal_data) != num_simulation_steps:
        original_time_axis = np.linspace(0, total_duration_s, len(analog_signal_data), endpoint=False)
        resampled_signal = np.interp(simulation_time_axis, original_time_axis, analog_signal_data)
    else:
        resampled_signal = analog_signal_data.copy()

    output_spike_train = np.zeros(num_simulation_steps, dtype=int)

    # Chuẩn hóa tín hiệu về khoảng [0, 1] để tính toán tốc độ
    min_val = np.min(resampled_signal)
    max_val = np.max(resampled_signal)

    if max_val == min_val: # Xử lý trường hợp tín hiệu không đổi
        normalized_input = np.ones_like(resampled_signal) * 0.5 if max_val > 0 else np.zeros_like(resampled_signal)
    else:
        normalized_input = (resampled_signal - min_val) / (max_val - min_val)

    instantaneous_rate_hz = normalized_input * peak_frequency_hz

    for i in range(num_simulation_steps):
        prob_of_spike = instantaneous_rate_hz[i] * time_step_s
        if np.random.rand() < prob_of_spike:
            output_spike_train[i] = 1

    return output_spike_train, simulation_time_axis, resampled_signal


def run_signal_encoding_demonstrations():
    """Tạo và vẽ đồ thị các ví dụ về mã hóa tốc độ."""
    print("--- Phần 1: Minh họa Chuyển đổi Tín hiệu sang Xung ---")
    sim_dt = 0.001  # Bước thời gian 1 ms
    total_time = 1.0  # Tổng thời gian 1 giây
    max_rate = 100  # Tần số xung tối đa 100 Hz

    # Ví dụ 1: Tín hiệu hình sin
    # Tạo trục thời gian có độ phân giải cao hơn cho tín hiệu gốc
    original_time_points = np.linspace(0, total_time, int(total_time / (sim_dt / 4)), endpoint=False)
    sine_wave_signal = 0.5 * (1 + np.sin(2 * np.pi * 2 * original_time_points)) # Tần số 2Hz, dịch chuyển để dương

    spikes_sine, time_sine, interp_sine = convert_timeseries_to_poisson_spikes(
        sine_wave_signal, total_time, sim_dt, max_rate
    )

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(original_time_points, sine_wave_signal, label="Tín hiệu Hình Sin Gốc", color='deepskyblue')
    # plt.plot(time_sine, interp_sine, label="Tín hiệu Nội suy", color='lightcoral', linestyle=':') # Tùy chọn: hiển thị tín hiệu nội suy
    plt.title("Mã hóa Tốc độ: Tín hiệu Hình Sin sang Chuỗi Xung Poisson")
    plt.ylabel("Biên độ Tín hiệu")
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.subplot(2, 1, 2)
    plt.eventplot(time_sine[spikes_sine == 1], linelengths=0.7, colors='darkblue', linewidths=1.5)
    plt.xlabel("Thời gian (giây)")
    plt.ylabel("Xung Tạo ra")
    plt.yticks([])
    plt.xlim(0, total_time)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Ví dụ 2: Tín hiệu bậc thang (Step Function)
    num_original_points_step = 200
    step_signal = np.zeros(num_original_points_step)
    step_signal[num_original_points_step // 4 : 3 * num_original_points_step // 4] = 0.8 # Bậc thang từ 25% đến 75% thời gian

    spikes_step, time_step, interp_step = convert_timeseries_to_poisson_spikes(
        step_signal, total_time, sim_dt, max_rate
    )

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    original_time_step = np.linspace(0, total_time, len(step_signal), endpoint=False)
    plt.plot(original_time_step, step_signal, label="Tín hiệu Bậc Thang Gốc", color='limegreen')
    plt.title("Mã hóa Tốc độ: Tín hiệu Bậc Thang sang Chuỗi Xung Poisson")
    plt.ylabel("Biên độ Tín hiệu")
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.subplot(2, 1, 2)
    plt.eventplot(time_step[spikes_step == 1], linelengths=0.7, colors='darkgreen', linewidths=1.5)
    plt.xlabel("Thời gian (giây)")
    plt.ylabel("Xung Tạo ra")
    plt.yticks([])
    plt.xlim(0, total_time)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    print("Kết thúc minh họa chuyển đổi tín hiệu sang xung.\n")


# --- Phần 2: Mô hình Tế bào Tích hợp Rò rỉ Phát Xung (LIF Đơn giản) ---
class SimpleLIFNeuron:
    """
    Một mô hình neuron Leaky Integrate-and-Fire (LIF) đơn giản hóa.
    """
    def __init__(self, tau_membrane_s=20e-3, R_membrane_Mohm=10.0,
                 v_threshold_mV=-50.0, v_reset_mV=-70.0,
                 v_resting_mV=-65.0, sim_dt_s=0.1e-3):
        """
        Khởi tạo tế bào phát xung.

        Args:
            tau_membrane_s (float): Hằng số thời gian màng (giây). Vd: 20ms
            R_membrane_Mohm (float): Điện trở màng (MegaOhms). Vd: 10 MOhms
            v_threshold_mV (float): Ngưỡng điện thế phát xung (mV). Vd: -50mV
            v_reset_mV (float): Điện thế reset sau xung (mV). Vd: -70mV
            v_resting_mV (float): Điện thế nghỉ của màng (mV). Vd: -65mV
            sim_dt_s (float): Bước thời gian mô phỏng (giây). Vd: 0.1ms
        """
        self.tau_m_s = tau_membrane_s
        self.R_m_ohm = R_membrane_Mohm * 1e6 # Chuyển đổi Mohm sang Ohm
        self.v_thresh_v = v_threshold_mV / 1000.0 # Chuyển mV sang V
        self.v_reset_v = v_reset_mV / 1000.0   # Chuyển mV sang V
        self.v_rest_v = v_resting_mV / 1000.0    # Chuyển mV sang V
        self.dt_s = sim_dt_s

        self.v_membrane_v = self.v_rest_v
        self.spike_times_s = []

    def step_dynamics(self, input_current_A, current_time_s):
        """
        Mô phỏng một bước thời gian cho tế bào.

        Args:
            input_current_A (float): Dòng điện đầu vào tại bước thời gian này (Amperes).
            current_time_s (float): Thời gian mô phỏng hiện tại.

        Returns:
            bool: True nếu một xung được tạo ra, False nếu không.
        """
        # Động học: tau_m * dV/dt = -(V - V_rest) + R_m * I_input
        dv_dt = (-(self.v_membrane_v - self.v_rest_v) + self.R_m_ohm * input_current_A) / self.tau_m_s
        self.v_membrane_v += dv_dt * self.dt_s

        has_fired = False
        if self.v_membrane_v >= self.v_thresh_v:
            self.v_membrane_v = self.v_reset_v  # Reset điện thế
            has_fired = True
            self.spike_times_s.append(current_time_s)
        return has_fired

    def reset_state(self):
        """Reset điện thế màng và thời gian xung đã ghi lại của tế bào."""
        self.v_membrane_v = self.v_rest_v
        self.spike_times_s = []

def demonstrate_lif_neuron_response():
    """Mô phỏng một tế bào LIF với một dòng kích thích và vẽ đồ thị phản ứng."""
    print("--- Phần 2: Mô phỏng Tế bào Phát Xung LIF ---")
    # Thuộc tính mô hình tế bào
    neuron_params = {
        'tau_membrane_s': 18e-3,     # 18 ms
        'R_membrane_Mohm': 12.0,      # 12 MOhms
        'v_threshold_mV': -52.0,      # -52 mV
        'v_reset_mV': -72.0,          # -72 mV
        'v_resting_mV': -68.0,        # -68 mV
        'sim_dt_s': 0.1e-3            # 0.1 ms
    }
    neuron = SimpleLIFNeuron(**neuron_params)

    # Thiết lập mô phỏng
    simulation_duration_s = 0.30  # 300 ms
    time_axis_s = np.arange(0, simulation_duration_s, neuron_params['sim_dt_s'])

    # Dòng điện đầu vào: Tăng dần rồi giảm dần (tam giác)
    input_current_A = np.zeros_like(time_axis_s)
    peak_current_nA = 2.0  # nA
    ramp_start_s = 0.05
    ramp_peak_s = 0.15
    ramp_end_s = 0.25

    idx_start = int(ramp_start_s / neuron_params['sim_dt_s'])
    idx_peak = int(ramp_peak_s / neuron_params['sim_dt_s'])
    idx_end = int(ramp_end_s / neuron_params['sim_dt_s'])

    # Đoạn tăng
    if idx_peak > idx_start:
        input_current_A[idx_start:idx_peak] = np.linspace(0, peak_current_nA * 1e-9, idx_peak - idx_start)
    # Đoạn giảm
    if idx_end > idx_peak:
       input_current_A[idx_peak:idx_end] = np.linspace(peak_current_nA * 1e-9, 0, idx_end - idx_peak)


    membrane_potential_history_mV = []
    neuron.reset_state() # Đảm bảo trạng thái ban đầu

    for t_idx, t_s in enumerate(time_axis_s):
        membrane_potential_history_mV.append(neuron.v_membrane_v * 1000) # Lưu trữ bằng mV
        neuron.step_dynamics(input_current_A[t_idx], t_s)

    plt.figure(figsize=(12, 8)) # Kích thước lớn hơn một chút
    ax1 = plt.gca()

    # Vẽ điện thế màng
    ax1.plot(time_axis_s * 1000, membrane_potential_history_mV, label="Điện thế màng (Vm)", color='teal')
    ax1.scatter(np.array(neuron.spike_times_s) * 1000,
                [neuron_params['v_threshold_mV']] * len(neuron.spike_times_s),
                color='red', marker='o', s=80, label="Sự kiện Xung", zorder=5)

    ax1.set_xlabel("Thời gian (ms)")
    ax1.set_ylabel("Điện thế màng (mV)", color='teal')
    ax1.tick_params(axis='y', labelcolor='teal')

    # Vẽ các đường ngưỡng
    ax1.axhline(neuron_params['v_threshold_mV'], color='salmon', linestyle='--', label=f"Ngưỡng ({neuron_params['v_threshold_mV']}mV)")
    ax1.axhline(neuron_params['v_reset_mV'], color='plum', linestyle='--', label=f"Reset ({neuron_params['v_reset_mV']}mV)")
    ax1.axhline(neuron_params['v_resting_mV'], color='lightgreen', linestyle='--', label=f"Nghỉ ({neuron_params['v_resting_mV']}mV)")

    # Vẽ dòng điện đầu vào trên trục y thứ hai
    ax2 = ax1.twinx()
    ax2.plot(time_axis_s * 1000, input_current_A * 1e9, color='gray', linestyle=':', alpha=0.8, label="Dòng kích thích (nA)")
    ax2.set_ylabel("Dòng kích thích (nA)", color='gray')
    ax2.tick_params(axis='y', labelcolor='gray')

    plt.title("Phản ứng của Tế bào LIF với Dòng Kích thích Hình Tam giác")

    # Kết hợp legend từ cả hai trục
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='lower right')

    ax1.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.show()
    print("Kết thúc mô phỏng tế bào phát xung.\n")


# --- Phần 3: Điều chỉnh Trọng số Synaptic qua Thời điểm Xung (Giống STDP) ---
def calculate_stdp_weight_delta(
    dt_post_minus_pre_s,
    A_plus=0.02, tau_plus_s=20e-3,  # LTP
    A_minus=0.022, tau_minus_s=22e-3 # LTD
):
    """
    Tính toán sự thay đổi trọng số synaptic dựa trên quy tắc STDP.

    Args:
        dt_post_minus_pre_s (float): Chênh lệch thời gian (t_post_spike - t_pre_spike) tính bằng giây.
        A_plus (float): Biên độ cho Hiện tượng Tăng cường Dài hạn (LTP).
        tau_plus_s (float): Hằng số thời gian cho LTP (giây).
        A_minus (float): Biên độ cho Hiện tượng Suy giảm Dài hạn (LTD).
        tau_minus_s (float): Hằng số thời gian cho LTD (giây).

    Returns:
        float: Thay đổi trọng số synaptic (delta_weight).
    """
    if dt_post_minus_pre_s > 1e-9:  # Xung pre trước xung post (gây LTP)
        return A_plus * np.exp(-dt_post_minus_pre_s / tau_plus_s)
    elif dt_post_minus_pre_s < -1e-9:  # Xung post trước xung pre (gây LTD)
        # dt_post_minus_pre_s là âm ở đây
        return -A_minus * np.exp(dt_post_minus_pre_s / tau_minus_s) # Lưu ý: dt_post_minus_pre_s là âm
    else: # Gần như đồng thời
        return (A_plus - A_minus) * 0.05 # Hiệu ứng nhỏ, có thể bằng không


def visualize_stdp_rule_and_evolution():
    """Minh họa cửa sổ học STDP và một ví dụ về sự tiến triển của trọng số."""
    print("--- Phần 3: Minh họa Đặc tính STDP ---")
    # Tham số quy tắc STDP
    ltp_amplitude = 0.05
    ltp_decay_s = 15e-3
    ltd_amplitude = 0.055 # LTD hơi mạnh hơn một chút để cân bằng
    ltd_decay_s = 18e-3

    # 1. Vẽ đồ thị cửa sổ học STDP (đường cong đặc tính)
    time_diffs_s = np.linspace(-70e-3, 70e-3, 300)  # -70ms đến +70ms
    weight_changes = [calculate_stdp_weight_delta(dt, ltp_amplitude, ltp_decay_s, ltd_amplitude, ltd_decay_s) for dt in time_diffs_s]

    plt.figure(figsize=(10, 5))
    plt.plot(time_diffs_s * 1000, weight_changes, color='darkviolet', linewidth=2.5)
    plt.axhline(0, color='k', linestyle=':', lw=1.2)
    plt.axvline(0, color='k', linestyle=':', lw=1.2)
    plt.title("Cửa sổ Học STDP (Thay đổi Trọng số $\Delta W$)")
    plt.xlabel("Chênh lệch Thời gian Xung $\Delta t = t_{post} - t_{pre}$ (ms)")
    plt.ylabel("Thay đổi Trọng số $\Delta W$")
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # 2. Minh họa sự tiến triển của trọng số synaptic qua nhiều cặp xung
    initial_weight = 0.5
    current_weight = initial_weight
    weight_history = [current_weight]

    # Định nghĩa một chuỗi các chênh lệch thời gian xung (giá trị delta_t tính bằng giây)
    # Ví dụ: pre phát xung trước post 10ms (LTP), post trước pre 15ms (LTD), ...
    spike_pair_time_diffs_s = [10e-3, -15e-3, 5e-3, -20e-3, 12e-3, -8e-3, 25e-3, -22e-3, 3e-3, -5e-3]

    print(f"Trọng số synaptic ban đầu: {initial_weight:.4f}")
    for i, dt_s in enumerate(spike_pair_time_diffs_s):
        delta_w = calculate_stdp_weight_delta(dt_s, ltp_amplitude, ltp_decay_s, ltd_amplitude, ltd_decay_s)
        current_weight += delta_w
        # Giới hạn trọng số (ví dụ: trong khoảng 0.01 đến 1.5)
        current_weight = np.clip(current_weight, 0.01, 1.5)
        weight_history.append(current_weight)
        print(f"Cặp Xung {i+1}: $\Delta t = {dt_s*1000:.1f}$ ms, $\Delta W = {delta_w:.4f}$, Trọng số Mới = {current_weight:.4f}")

    plt.figure(figsize=(10, 5))
    plt.plot(range(len(weight_history)), weight_history, marker='s', linestyle='--', color='coral', markersize=6)
    plt.title("Sự Tiến triển Trọng số Synaptic qua Nhiều Cặp Xung")
    plt.xlabel("Thứ tự Cặp Xung")
    plt.ylabel("Giá trị Trọng số Synaptic")
    plt.xticks(range(len(weight_history)))
    plt.ylim(0, max(1.5, np.max(weight_history) * 1.1)) # Điều chỉnh giới hạn y
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.show()
    print("Kết thúc minh họa đặc tính STDP.\n")


if __name__ == "__main__":
    run_signal_encoding_demonstrations()
    demonstrate_lif_neuron_response()
    visualize_stdp_rule_and_evolution()